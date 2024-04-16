---
title: 'LiGuard: A GUI-powered Python Framework for Processing Point-Cloud Data'

tags:
  - Python
  - GUI
  - Open3D
  - OpenCV
  - LiDAR
  - Point-Cloud Processing
  - Image Processing
  - Visualization
authors:
  - name: Muhammad Shahbaz
    orcid: 0009-0003-6377-8274
    affiliation: 1
  - name: Shaurya Agarwal
    orcid: 0000-0001-7754-6341
    affiliation: 1
affiliations:
  - name: University of Central Florida, USA
    index: 1
date: 16 April 2024
bibliography: paper.bib

---
# Summary
There is a growing interest in the development of LiDAR-based applications in domains like robotics, autonomous driving, traffic monitoring, infrastructure inspection, and many areas of envrionmental surveying and mapping. However, to conduct research in these areas, researchers often need to develop custom software for their case specific requirements, leading to duplication of efforts and lack of standardization. To address this issue, a GUI-powered Python framework, `LiGuard` is presented. `LiGuard` allows building dynamic point-cloud (and accompanying image) data processing pipelines by decoupling research algorithms from framework's source code. This dynamic design facilitates users in focusing on researching novelties rather than the intricacies of feature-complete software development. The decoupled design also aids ablation studies by providing researchers the ability to dynamically execute algorithms using a user-friendly GUI. Additionally, it allows them to incorporate editable parameters of their algorithms into the framework's interface, making it easier to fine-tune their algorithms interactively. `LiGuard` supports both individual (live) and bulk (batch) processing, thus facilitating testing and visual inspections on selected test cases before processing large-scale data.

# Statement of Need
The research on point-cloud data is challenging as the available libraries such as PCL [@Rusu_ICRA2011_PCL], Open3D [@Zhou2018], and other [@brown2012laspy; @pyntcloud; @Hunter:2007; @Lamprecht2019], etc. focus single point-cloud frames, and although some efforts such as [@Goelles2021] attend to processing bulk data, the focus is still developing a python package that can be imported to custom, often hard-coded scripts, thus imposing limitations on reusability and scalability.

`LiGuard` tackles the issue by segregating the data processing pipeline from the application logic, making it a modular, reusable, and extensible framework. It is, at its core, a combination of five sub-modules, (1) Data I/O, (2) Process Configuration, (3) Inter-Process Data Sharing, (4) Data Processing, and (5) Visualization. During its development, a great focus is put towards abstracting away the tasks that foster duplication of efforts, therefore, Data I/O, Inter-Process Data Sharing, and Visualization sub-modules are developed in such a way that they, although allow modifications from development contributors, are running behind the curtains for researchers to relieve them of the burden of reading data efficiently, creating logic to keep the processing as interactive as possible (often requiring in-depth understanding of multi-threading), and visualizing (to some extent the) outcomes before starting bulk process loop, etc. This, in turn, allows researchers to focus on two main things of their point-cloud data processing pipelines, the processes they need to execute on the data and the configuration of those processes. `LiGuard` facilitates this by (a) providing YAML formatted configuration files that are later loaded into GUI allowing easy manipulations of the parameters, and (b) allowing researchers to directly create corresponding (to configuration) functions that are automatically called along with configuration parameters and data.

# Architecture
![`LiGuard`'s Architecture\label{fig:liguardarch}](figs/block_diagram.png){ width=80% }

`LiGuard` is built on top of the Open3D [@Zhou2018] and OpenCV [@opencv_library] libraries allowing researchers and contributors to leverage the extensive functionalities provided by these libraries. A high-level architecture is presented in \autoref{fig:liguardarch} consisting of five main components (related to the five sub-modules mentioned in [Section: Statement of Need](#statement-of-need)): (1) GUI (purple), (2) Data Handlers (green), (3) Shared Configuration Dictionary (blue), (4) Shared Data Dictionary (orange), and (5) Research Algorithms. The GUI component is responsible for creating a user-friendly interface for researchers to interact with the framework and for visualizations of both LiDAR and image data. The Data Handlers component is responsible for reading data from disk/sensor(s). The Shared Configuration Dictionary and Shared Data Dictionary components are responsible for sharing configuration and data between different components of the framework. The Research Algorithms component is responsible for implementing the algorithms that process the data. Please note that the research algorithms are analogous to the data processes mentioned in [Section: Statement of Need](#statement-of-need).

# Usage
A tutorial with technical details is available under [`Usage`](https://github.com/m-shahbaz-kharal/LiGuard-JOSS/tree/main?tab=readme-ov-file#usage) at our [`Github`](https://github.com/m-shahbaz-kharal/LiGuard-JOSS) repository. There, we demonstrate the capabilities of `LiGuard` by implementing a simple pipeline of processing samples from KITTI [@geiger2013vision] dataset. The pipeline incorporates reading point-cloud, image, and (KITTI's standard) label data, followed by cropping point-clouds, removing out-of-bound and low point-density labels, and storing the processed dataset in OpenPCDet[@openpcdet2020] standard.

# Contributions
M.S and S.A. conceived the idea of `LiGuard`. M.S. developed the framework, wrote the documentation, and wrote the manuscript. S.A. reviewed the manuscript and provided feedback. Both authors have read and agreed to the published version of the manuscript.

# Acknowledgements
We thank [Dr. Karan Sikka](https://www.ksikka.com) for his great support and guidance throughout the development of `LiGuard`.

# References
