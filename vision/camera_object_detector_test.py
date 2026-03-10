import pyrealsense2 as rs
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

#program variables
DB_epsilion = 0.05 #0.05 works well
DB_min_samples = 5 #5 works well
downsample = 1 #Only takes n-th point from the pointcloud (set to 1 for no downsampling)

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
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
pc = rs.pointcloud()
pipeline.start(config)

#Throw away the first 150 frames (5 seconds)
for _ in range(150):     
    pipeline.wait_for_frames()

#Capture a frame
frames = pipeline.wait_for_frames()
depth = frames.get_depth_frame()


#Create a matrix of points in form
#[x1, y1, z1]
#[x2, y2, z2]
#[xn, yn, zn]
verts = np.asanyarray(pc.calculate(depth).get_vertices()) #get verticies from realsense pointcloud
points = verts.view(np.float32).reshape(-1, 3)
points = points[:: downsample]

#Removes the planes using the AI generated plan detection function (to remove flors, walls, etc.)
plane, plane_inliers = fit_plane_ransac(
    points,
    n_iter=200,
    distance_thresh=0.01
)
points_objects = points[~plane_inliers]


#Clustering the points with DBSCAN to find objects
db = DBSCAN(DB_epsilion, DB_min_samples).fit(points_objects)
labels = db.labels_

n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print("Estimated number of objects %d" % n_clusters_)
print("Estimated number of noise points: %d" % n_noise_)



#Plot the clustered point clouds of detected objects as a 3D scatterplot.
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.scatter(-points_objects[:, 0], -points_objects[:, 1], -points_objects[:, 2], c=labels)

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("Detected object clusters")
plt.show()
