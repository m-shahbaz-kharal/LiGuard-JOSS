# Installing Sensor SDKs
To receive live data from sensors like LiDAR and cameras, the respective SDKs need to be installed. Currently, the only supported LiDAR sensors are [Ouster](https://ouster.com)'s `OS` series and [FLIR](https://www.flir.com)'s `BFS-PGE` series. The support for [ROS](https://www.ros.org)-based drivers is coming soon.
# Ouster SDK
Ouster is a LiDAR sensor manufacturer. They provide an SDK to interface with their sensors. The SDK as pip package can be installed using the following command:
```pip install ouster-sdk==0.10.0```
# Spinnaker-SDK
For FLIR cameras the Spinnaker SDK can be used. The SDK can be downloaded from the following link: [Spinnaker SDK](https://www.flir.com/support-center/iis/machine-vision/downloads/spinnaker-sdk-download/spinnaker-sdk--download-files/), it is a zip file that needs to be extracted. The wheel inside the extracted folder can be installed using the following command:
```pip install <wheel_name>.whl```