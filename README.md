# Confocal-NV-centers

The project we are currently working on is setting up a scanning confocal microscope for ODMR. Optically Detected Magnetic Resonance (ODMR) is a technique in which changes in the spin state of a system, such as NV centers in diamond, are detected by measuring changes in the intensity of the emitted fluorescence when a microwave field is applied. The fluorescence is emitted when the sample is irradiated with a pulsed green laser, and transitions between different spin states lead to corresponding variations in the observed fluorescence intensity. A scanning confocal microscopy setup isolates this signal, where a pinhole implemented using a fiber-optic cable removes out-of-focus light and enables point-by-point scanning. The scanning is carried out using galvo mirrors, and a LabVIEW program controls their motion, defines the scan pattern, and synchronizes the mirror movement with the photodetector. The fluorescence intensity at each scan position is recorded using a single-photon detector, while the laser excitation is pulsed independently using an acousto-optic modulator (AOM).

## LabVIEW inputs

Counter Path: Dev1/ctr0
Galvo mirror Path: Dev1/ao0:1
