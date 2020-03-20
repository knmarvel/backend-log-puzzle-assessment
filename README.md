# Log Puzzle
For the Log Puzzle exercise, you'll use Python code to solve two puzzles. This exercise uses the urllib module. Add your code to the `logpuzzle.py` file.

An image of an animal has been broken into many narrow vertical stripe images. The stripe images are on the internet somewhere, each with its own url. The urls are hidden in a web server log file. Your mission is to find the urls and download all image stripes to re-create the original image.

The slice urls are hidden inside apache log files (the open source [apache](http://httpd.apache.org/) web server is the most widely used server on the internet). Each log file is from some server, and the desired slice urls are hidden within the logs. The log file encodes what server it comes from like this: the log file `animal_code.google.com` is from the `code.google.com` server (formally, we'll say that the server name is whatever follows the first underbar). The `animal_code.google.com` log file contains the data for the "animal" puzzle image. Although the data in the log files has the syntax of a real apache web server, the data beyond what's needed for the puzzle is randomized data from a real log file.

Here is what a single line from the log file looks like (this really is what apache log files look like):
```
10.254.254.28 - - [06/Aug/2007:00:14:08 -0700] "GET /foo/talks/ HTTP/1.1"
200 5910 "-" "Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.4) Gecko/20070515 Firefox/2.0.0.4"
```
The first few numbers are the address of the requesting browser. The most interesting part is the "GET _path_ HTTP" showing the path of a web request received by the server. The path itself never contains spaces, and is separated from the GET and HTTP by spaces (regex suggestion: `\S` (upper case S) matches any non-space char). Find the lines in the log where the string "puzzle" appears inside the path, ignoring the many other lines in the log.

FIRST, set up main() so all it does is argparse and print the results from read_urls() and download_images

## Part A - Log File To Urls
-Complete the `read_urls(filename)` function that extracts the puzzle urls from inside a logfile with the following steps:
-Find all the "puzzle" path urls in the logfile.
//my breakdown of this step
-what is the logfile?
-it's a file used as a parameter on the command line. 
-see: animal_code.google.com and place_code.google.com files in our file explorer
-each logfile has hundreds of lines that look like this:
10.254.254.29 - - [06/Aug/2007:00:12:19 -0700] "GET /edu/languages/google-python-class/images/puzzle/p-bija-baei.jpg HTTP/1.0" 200 22950 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.12) Gecko/20070508 Firefox/1.5.0.12"
-from each line, we want the end of an URL that looks like this:
-"/edu/languages/google-python-class/images/puzzle/p-bija-baei.jpg"
-how do we open the file and save the data for manipulation?
-what kind of data did we just save?
-how can we split this string by line breaks?
-how do we get rid of lines that don't have the word "puzzle" in them?
	-oh crap regex
-how do we get rid of everything in the line except the end of the URL?
	-oh shit regex


-Combine the path from each url with the server name from the filename to form a full url, e.g. `http://www.example.com/path/puzzle/from/inside/file`.
-from above in this readme, "The log file encodes what server it comes from like this: the log file `animal_code.google.com` is from the `code.google.com` server (formally, we'll say that the server name is whatever follows the first underbar"
-how do we add "http://code.google.com" to the beginning of each item on our list?

-Screen out urls that appear more than once. 
-how do we get rid of duplicates in the list?

-The `read_urls()` function should return the list of full urls, sorted into alphabetical order and without duplicates. 
-how do we sort the list by alphabetical order?
(P.S., we'll be coming back to this step later to fix it, and you'll hate it.)
-how do we return our list of urls?

Taking the urls in alphabetical order will yield the image slices in the correct left-to-right order to re-create the original animal image. In the simplest case, main() should just print the urls, one per line.
-how do we print the returned value from read_urls line by line?
(HA! solved for us in the starter code.)


```console
$ python logpuzzle.py animal_code.google.com
http://code.google.com/something/puzzle-animal-baaa.jpg
http://code.google.com/something/puzzle-animal-baab.jpg
...
```

## Part B - Download Images Puzzle
-Complete the `download_images()` function which takes a sorted list of urls and a destination directory. 
-we create that sorted list of urls with the read_urls() function
-we give the destination directory as a parameter when we run it from the command line.

-creating the directory first if necessary (see the "os" module to create a directory)
-how do we check to see if a directory exists?
-how do we create a dirctory if it doesn't exist?

-download the image from each url into the given directory (see the `urllib.urlretrieve()` for downloading a url)
-how do we download each url in the list? 
-look up urllib.urlretrieve usage
-urlretrieve(url_to_download, destination_directory/image_name)
-Name the local image files with a simple scheme like "img0", "img1", "img2", and so on. 
-how do we name the images with numbers in order?
-You may wish to print a helpful "Retrieving..." status output line while downloading each image since it can be slow and its nice to have some indication that the program is working. 
how do we print "Retrieving..." and the image name for each image?



Each image is a little vertical slice from the original. 

How to put the slices together to re-create the original? It can be solved nicely with a little html (knowledge of HTML is not required).

-The `download_images()` function should also create an index.html file in the directory with an <img> tag to show each local image file. 
-The img tags should all be on one line together without separation. In this way, the browser displays all the slices together seamlessly. You do not need knowledge of HTML to do this;
-just create an index.html file that looks like this:

```
<html>
<body>
<img src="/edu/python/exercises/img0"><img src="/edu/python/exercises/img1"><img src="/edu/python/exercises/img2">...
</body>
</html>
```
Of course your index file won't actually use the `/edu/python/exercises/` src path for images; it will use the directory path specified in the `--todir` cmd line option. 

///OK WHAT???
-OK, so now we need to either look through the directory for the image files we just saved, OR go back and create this index.html file as we save each file. Let's do the second thing. our download_images() function should do ALL OF THE FOLLOWING:
-takes a sorted list of urls and a destination directory as parameters
-create the directory first if necessary
-save the text that starts an index.html file as a variable
-have a loop through the list of urls that:
-creates a specific name for the image
-downloads the image from each url into the given directory with the specific name
-adds an image tag to the text that will become an index.html file with the current image's directory path as the image source
-add the ending tags to the text that will become the index.html file
-create and write the text to the index.html file 

Here's what it should look like when you can download the animal puzzle:

```
$ python logpuzzle.py --todir animaldir animal_code.google.com
$ ls animaldir
img0 img1 img2 img3 img4 img5 img6 img7 img8 img9 index.html
```

When it's all working, opening the index.html in a browser should reveal the original animal image. What is the animal in the image?

<img src="https://i.ytimg.com/vi/SxvyKqkCXy0/maxresdefault.jpg" width="300" />

## Part C - Image Slice Descrambling
The second puzzle involves an image of a very famous place, but depends on some custom sorting. For the first puzzle, the urls can be sorted alphabetically to order the images correctly. In the sort, the whole url is used. However, we'll say that if the url ends in the pattern `-_wordchars-wordchars_.jpg`, e.g. `http://example.com/foo/puzzle/bar-abab-baaa.jpg`, then the url should be represented by the **second** word in the sort (e.g. "baaa"). So sorting a list of urls each ending with the word-word.jpg pattern should order the urls by the second word.

Extend your code to order such urls properly, and then you should be able to decode the second place_code.google.com puzzle which shows a famous place. What place does it show?

//OK, WHAT???? Now we have to go back to the read_urls() function.
-the urls should be sorted alphabetically by the word that comes before the jpg. 
-how do we sort?
-how do we sort specifically using the word that comes before .jpg in a string????
-oh fuck regex.


## Guidance
- We are looking for readable, maintainable, performant code. Appropriate comments are expected.
- Your solution must pass a PEP8 (flake8) check with 0 errors reported.
- You must use at least one regular expression in your solution somewhere.
- Your solution must use the 'with' statement (Python context manager).
- You must use the `if __name__ == '__main__'` Python idiom, and define a main() function.
- It is *OKAY* to add your own helper functions to achieve a solution!
- You will need an active internet connection in order to download the images. 
- If your socket connection times out within urllib, try again.

## Workflow for this Assignment
1. Fork this repository into your own personal github account.
2. Then Clone your own repo to your local development machine.
3. Create a separate branch named dev/your-github-username, and checkout the branch.
4. Commit your changes, then git push the branch back to your own github account.
5. From your own Github repo, create a pull request (PR) from your dev branch back to your own master.
6. Copy/Paste the URL link to your PR as your assignment submission.

## Credits
Creative Commons (CC) Attribution: The images used in this puzzle were made available by their owners under the [Creative Commons Attribution 2.5](http://creativecommons.org/licenses/by/2.5/) license, which generously encourages remixes of the content such as this one. The animal image is from the user zappowbang at flickr and the place image is from the user booleansplit at flickr.