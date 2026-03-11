import pyrealsense2 as rs
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

#program variables
DB_epsilion = 0.01 #0.05 works well
DB_min_samples = 10 #5 works well
downsample = 1 #Only takes n-th point from the pointcloud (set to 1 for no downsampling)
shutter_delay = 3 #seconds
camera_fps = 5
resolution = [640, 480]
object_min_points = 0 #Objects from clusters with less points that this are removed (set to 0 to enable dynamic scaling)
object_min_points_scale = 0.5 #Dynamic scaling of min objects based on max depth from camera

the_cheese_flag = False #Important

#Function AI generated
def fit_plane_ransac(points, n_iter=150, distance_thresh=0.01):
    """
    Fit a plane ax + by + cz + d = 0 with simple RANSAC.
    Returns:
        best_plane: (4,) array [a, b, c, d]
        inlier_mask: boolean mask of points belonging to the plane
    """
    if len(points) < 3:
        return None, np.zeros(len(points), dtype=bool)

    best_inliers = np.zeros(len(points), dtype=bool)
    best_plane = None
    best_count = 0

    rng = np.random.default_rng()

    for _ in range(n_iter):
        idx = rng.choice(len(points), size=3, replace=False)
        p1, p2, p3 = points[idx]

        v1 = p2 - p1
        v2 = p3 - p1
        normal = np.cross(v1, v2)
        norm = np.linalg.norm(normal)

        if norm < 1e-8:
            continue

        normal = normal / norm
        d = -np.dot(normal, p1)

        distances = np.abs(points @ normal + d)
        inliers = distances < distance_thresh
        count = np.count_nonzero(inliers)

        if count > best_count:
            best_count = count
            best_inliers = inliers
            best_plane = np.array([normal[0], normal[1], normal[2], d])

    return best_plane, best_inliers


#Create the pipeline from camera to python
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, resolution[0], resolution[1], rs.format.z16, camera_fps)
pc = rs.pointcloud()
pipeline.start(config)

#Throw away the first couple of frames as the camera adjusts itself
s = 0
for i in range(shutter_delay*camera_fps):
    if((shutter_delay - s == 0) and (the_cheese_flag)):
        print("Say cheese!")
        the_cheese_flag = False
    if(i % camera_fps == 0):
        print(shutter_delay - s)
        s += 1
        the_cheese_flag = True

    pipeline.wait_for_frames()

#Capture a frame
frames = pipeline.wait_for_frames()
depth = frames.get_depth_frame()

print("Processing the image...")

#Create a matrix of points in form
#[x1, y1, z1]
#[x2, y2, z2]
#[xn, yn, zn]
verts = np.asanyarray(pc.calculate(depth).get_vertices()) #Gets verticies from pyrealsense2 pointcloud
points = verts.view(np.float32).reshape(-1, 3)
points = points[~np.all(points == 0, axis=1)] #Removes invalid point data
points = points[:: downsample]

#Removes the planes using the AI generated plan detection function (to remove flors, wallSs, etc.)
plane, plane_inliers = fit_plane_ransac(
    points,
    n_iter=200,
    distance_thresh=0.01
)
points_objects = points[~plane_inliers]


#Clustering the points with DBSCAN to find objects
db = DBSCAN(eps=DB_epsilion, min_samples=DB_min_samples).fit(points_objects)
labels = db.labels_

n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print("Estimated number of objects %d" % n_clusters_)
print("Estimated number of noise points: %d" % n_noise_)

#Removes the noise from the data set
points_objects = points_objects[labels != -1]
labels = labels[labels != -1]

#Removes obect wit too few points
unique_labels, points_per_object = np.unique(labels, return_counts=True)
print("Points per object cluster", points_per_object)
temp_points = np.array([])
temp_labels = np.array([])
if (object_min_points == 0):
    object_min_points = (2000/(np.max(points_objects[:, 2])))*object_min_points_scale/downsample
    print("Dynamic minimal points per cluster to qualify as an object: ", object_min_points)

for i in range(len(points_objects)):
    idx = np.where(unique_labels==labels[i])[0][0]
    
    if(points_per_object[idx] > object_min_points):
        temp_points = np.append(temp_points, points_objects[i])
        temp_labels = np.append(temp_labels, labels[i])
labels = temp_labels
points_objects = np.reshape(temp_points, (-1, 3))

#Find centers of objects
centroids = np.array([])
for j in np.unique(labels):
    points_of_cluster= points_objects[labels==j,:]
    centroids = np.append(centroids, np.mean(points_of_cluster, axis=0))
centroids = np.reshape(centroids, (-1, 3))


if(points_objects.size != 0):
#Plot the clustered point clouds of detected objects as a 3D scatterplot.
    fig = plt.figure(figsize=(14,6))
    ax = fig.add_subplot(1, 2, 1, projection="3d")

    ax.scatter(points_objects[:, 0], -points_objects[:, 1], -points_objects[:, 2], c=labels) #'z' need to be inverted since the camera measures depth and is looking down, 'y' also needs to be inverted for the plot to match reality but I dunno why
    ax.scatter(centroids[:, 0], -centroids[:, 1], -centroids[:, 2], marker='x', c='black', s=100, linewidths=2, label="Centroids")

    ax.set_xlim(np.min(points_objects[:, 0])-0.1, np.max(points_objects[:, 0])+0.1)
    ax.set_ylim(-(np.max(points_objects[:, 1])+0.1), -(np.min(points_objects[:, 1])-0.1))
    ax.set_zlim(-np.max(points_objects[:, 2]), 0)
    
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Detected object clusters")

    ax2 = fig.add_subplot(1,2,2)
    ax2.scatter(points_objects[:, 0], -points_objects[:, 1], c=labels) #'z' need to be inverted since the camera measures depth and is looking down, 'y' also needs to be inverted for the plot to match reality but I dunno why
    ax2.scatter(centroids[:, 0], -centroids[:, 1], marker='*', color='white', edgecolor='black', s=200, label="Centroids")

    ax2.set_xlabel("X")
    ax2.set_ylabel("Y")
    ax2.grid()
    ax2.set_title("2D projection")
    ax2.legend()

    plt.show()
else: print("No objects detected!")
