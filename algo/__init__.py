"""
The algo package contains implementations of various algorithms for the data processing pipeline. It also includes built-in algorithms that can be utilized within the pipeline.

### Modules and Their Purposes:

- **algo.pre**: Contains generic pre-processing algorithms for data, such as augmentation and normalization.
- **algo.lidar**: Contains algorithms for point cloud processing.
- **algo.camera**: Contains algorithms for image processing.
- **algo.calib**: Contains algorithms for manipulating calibration parameters, like rectification and sensor fusion.
- **algo.label**: Contains algorithms for manipulating both read and predicted labels, including filtering based on criteria.
- **algo.post**: Contains generic post-processing algorithms, like saving data in specific formats or directories.

### Execution Order:

The order of execution for algorithms within each sub-module is determined by the `priority` parameter in the `config.yml` file. Lower priority values correspond to earlier execution. This parameter can be modified in the GUI configuration window.

The overall order of execution across sub-modules follows this sequence: pre -> lidar -> camera -> calib -> label -> post.

### Implementing a New Algorithm:

To implement a new algorithm, follow these steps:

1. Add a YAML configuration entry in the `config.yml` file under the appropriate sub-module (`proc:<module>`).
2. Implement the algorithm function in the corresponding file within the algo package.

#### Example YAML Entry:

```yaml
proc:
  lidar:
    dummy:
      enabled: True
      priority: 1
      other_param_1: 0
      other_param_2: hello
      other_param_3: True
      other_param_4: [1, 2, 3]
      other_param_5: {key1: value1, key2: value2}
```

Algorithm Function Signature:
```python

def dummy(data_dict: dict, cfg_dict: dict):
    '''
    Args:
        data_dict (dict): A dictionary containing the data in the pipeline.
        cfg_dict (dict): A dictionary containing configuration parameters from config.yml.

    Returns:
        None
    '''
    # Getting logger object from data_dict
    logger = data_dict.get('logger')
    if logger is None:
        print('[CRITICAL ERROR]: No logger object in data_dict. Abnormal behavior detected.')
        return

    # Checking for required data in data_dict
    if 'current_point_cloud_path' not in data_dict:
        logger.log('[algo->lidar.py->dummy]: current_point_cloud_path not found in data_dict', Logger.DEBUG)
    
    if 'current_point_cloud_numpy' not in data_dict:
        logger.log('[algo->lidar.py->dummy]: current_point_cloud_numpy not found in data_dict', Logger.ERROR)
        return

    # Accessing required data from data_dict
    current_point_cloud_path = data_dict['current_point_cloud_path']
    current_point_cloud_numpy = data_dict['current_point_cloud_numpy']

    # Perform operations with the data and update data_dict
    # ...
 
```

"""