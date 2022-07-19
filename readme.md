<h1>Description</h1>
<p>
   Simple interface for demonstraiting computer vision. Designed as a mockup for a disaster recovery robot program to detect humans in a disaster area. 
   Created with python, OpenCv, numpy, and PyQt5. Training photos sourced from google open image. 
</p>
<h1>Getting Started</h1>
<p>
   Requirements:
      Python version must be 3 and higher.
   To install additional requirements:
   <ul>
    <li>note: You may wish to perform this in a virtual enviroment as there are quite a few modules.</li>
    <li>Open a terminal in the root directory</li>
    <li>Run the command "pip install -r requirements.txt"</li>
   </ul>
</p>

<h1>Getting started</h1>
<ul>
   <li>To begin in the command terminal type "python main.py [program you wish to use] " select the program you wish to use {train or demo}</li>
   <li>Then set the associated falgs. for a list of available flags enter "python main.py -h or --help"</li>
   <li>To view the provided demo enter "python main.py demo -p"<li>
   <li>for training instructions see <a href="#training">Training</a></li>
</ul>

<h1 id="training">Training</h1>
<p>To begin trainining your own model. In the terminal enter "python main.py train --folderPath <Path> --trainSize <int>".
   A label image gui will automatically pop up. you will select either the test or train folder from this program to begin adding your bounding boxes. 
   Be sure to change your save dir (under file->change save dir) to the same folder you are working on. Once finished you will get another pop-up to do the remaining folder.
   Note: Use only PascalVoc for annotaion. For useful information on how to use this tool press help and view the tutorials.
</p>
<ul>
  <li>If there are images you do not want to use just do not place bounding boxes and they will be removed.</li>
  <li>The xml files created are removed by the program after they are converted to csv.</li>
  <li></li>
</ul>




