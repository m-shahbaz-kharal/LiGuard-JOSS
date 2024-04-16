# Built-in Utility Functions
In `algo/lidar.py` (or in configuration under `proc/lidar`):
- crop: Crops a point cloud
- project_image_pixel_colors: Projects pixel colors from an image to a point cloud, requires calib and image data

In `algo/camera.py` (or in configuration under `proc/camera`):
- project_point_cloud_points: Overlays a point cloud on an image, requires calib and point cloud data

In `algo/label.py` (or in configuration under `proc/label`):
- remove_out_of_bound_labels: Removes labels that are out of bound of the crop-bound defined in `proc/lidar/crop`

In `algo/post.py` (or in configuration under `proc/post`):
- create_per_object_pcdet_dataset: Extract point-clouds and corresponding bounding-box for each object in a frame, saves point-clouds in .npy format and labels in OpenPCDet annotation format, requires point-cloud and label data
- create_pcdet_dataset: Saves the processed point-cloud data in .npy format and labels in OpenPCDet format, requires point-cloud and label data

## Auxiliary Utility Functions
There are some utility functions that are not processing functions but are used in the processing functions. These functions are defined in `algo/utils.py` and can be imported in any processing function. The utility functions are:
- gather_point_clouds: Gathers `current_point_cloud_numpy` in `data_dict` and stores in an array in `data_dict` using a `key` and `couunt` (as the number of point clouds to gather). An argument `global_index_key` can be used if need to make sure that only previously ungathered point clouds are gathered.
- combine_gathers: Combines gathered point clouds in `data_dict` using a `global_index_key` and stores them as single array in `data_dict` at index `key`.
- skip_frames: Skips `skip` number of frames in a sequence of frames. An argument `global_index_key` can be used if need to make sure that only previously unskipped frames are skipped.