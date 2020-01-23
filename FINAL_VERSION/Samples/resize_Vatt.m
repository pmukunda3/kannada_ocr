clc
clear
close 

pkg load image
srcdir = 'Unresized/Vattaksharas';
dir1 = 'Vatt15';
dir2 = 'Vatt20';
dir3 = 'Vatt30';
mkdir(dir1);
mkdir(dir2);
mkdir(dir3);
files = readdir(srcdir);
for i = 3:length(files)
  img = imread([srcdir '/' files{i}]);
  [H,W] = size(img);
  ar = W/H;
  W15 = ar*15;
  if W15 <= 22 
    img2 = imresize(img,[15 15],'cubic');
    #img2 = img;
    imwrite(img2,[dir1 '/' files{i}]);
  end
  if W15 >= 18 && W15 <= 27
    img2 = imresize(img,[15 20],'cubic');
    #img2 = img;
    imwrite(img2,[dir2 '/' files{i}]);
  end
  if W15 >= 23 
    img2 = imresize(img,[15 30],'cubic');
    #img2 = img;
    imwrite(img2,[dir3 '/' files{i}]);
  end
end