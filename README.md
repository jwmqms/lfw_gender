# lfw_gender (Labeled Faces in the Wild - Gender Classification)
## Intro
This is a suite for performing gender classification on the LFW dataset in both
software and hardware. All software is in Python and the hardware is in VHDL.
## Prerequisites
### Software
[Python 2.7.X](https://www.python.org/downloads/release/python-279/) (all other
versions are untested)

[Numpy] (http://www.numpy.org/)

[matplotlib] (http://matplotlib.org/)

[requests] (http://docs.python-requests.org/en/latest/) - Only required if the
genders are being updated.

[scipy] (http://www.scipy.org/) - Only required if you are redoing the image
processing.

If you are new to Python, it is recommended that you use the following
procedure to obtain the dependencies:

1) If you don't have pip (check in your Python27/Scripts folder) obtain it
from [here](https://pip.pypa.io/en/latest/installing.html).

2) Install the dependencies using pip:
`pip install numpy matplotlib requests scipy`
### Hardware
1) VHDL compiler, simulator, and autolayout tool. This project used Mentor
Graphic's Pyxis' suite:

	a) VSIM: VHDL compilation and simulation
	
	b) Pyxis: Autolayout
	
	c) Calibre: Power extraction
	
	d) Eldo: SPICE simulation

## Usage
### Software
Download this repo and inside the "src/python" folder execute
`python setup.py install`.

This package is platform independent, and should work on any system running
Python 2.7.X.

Click [here](http://techtorials.me/lfw_gender/index.html) to access the API.
#### Initial workflow
0) Build the project.
	
	a) Inside the repo go to "src/python".
	
	b) Execute `python setup.py install`.

1) Generate the updated genders.
	
	a) Inside the repo go to "src/python/lfw_gender".
	
	b) Execute `python get_genders.py`. You should have the file
	"data/genders.csv", which is a list of first names and genders.

2) Preprocess the data.
	
	a) Inside the repo go to "src/python/lfw_gender".
	
	b) Execute `python preporcess.py`. You should have a folder	
	"data/preprocessed". Inside of that folder there should be a "male" and
	"female" folder. Inside each of those folders will be a pickled file
	containing the preprocessed image. Note that these files are not deleted.
	If you update the genders, you should delete all of those pickle files and
	update them again. If you don't update the images, but change the
	preprocessing, the files will be overwritten automatically.

3) Split the data.
	
	a) Inside the repo go to "src/python/lfw_gender".
	
	b) Execute `python split_data.py`. The pickle file 
		"src/python/lfw_gender/data/lfw.pkl" will be created. The file will
		have the data stored in the format of:
		(train_x, train_y), (test_x, test_y).

4) Rebuild the project. After this step, you can use the updated images as you
normally would. They will be included in the package.
	
	a) Inside the repo go to "src/python".
	
	b) Execute `python setup.py install`.

### Hardware
Create a new project, link to the code in the "src/vhdl" folder and proceed as
you would with any other project.

## Preprocessing
1) The utilized LFW dataset was the frontalized one obtained from
[here](http://www.openu.ac.il/home/hassner/projects/frontalize/).

2) The genders were obtained by using the [genderize.io](https://genderize.io/)
API. Only genders with > 90% confidence interval were selected. All images
containing valid genders were used as the base set.

3) The images in the base set were converted to grayscale.

4) The images in the base set were resized from 90x90 to 30x30 and then
reshaped to be a vector of length 900.

5) For each person in the base set, a single image was randomly selected to
form the new base set.

6) From the new base set, the 500 random females and 500 random males were
selected to form the full dataset.

7) 400 females and 400 males were randomly selected from the full dataset to
create the training / validation set. The remaining 100 females and 100 males
were used as the testing set.

## Authors
The original authors of this code are James Mnatzaganian and Qutaiba Saleh. For
contact info, as well as other details, see James' corresponding
[website](http://techtorials.me). James is the primary contact for the software
/ algorithm and Qutaiba is the primary contact for the hardware.

## Legal
This code is licensed under the [MIT license](http://opensource.org/licenses/
mit-license.php). The dataset we are using originated from [here]
(http://vis-www.cs.umass.edu/lfw/). Additionally, we are using a preprocessed,
frontalized, version of this dataset, which was obtained from
[here](http://www.openu.ac.il/home/hassner/projects/frontalize/). Please
refer to the licensing of those datasets for more details. These authors claim
no ownership of those datasets and merely provided the dataset for convenience
purposes, only.