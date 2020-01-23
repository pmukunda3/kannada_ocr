clc
clear
close 

pkg load image
srcdir = 'Unresized/Samples_Gray';
dir1 = 'Samples15';
dir2 = 'Samples25';
dir3 = 'Samples30';
dir4 = 'Samples40';
mkdir(dir1);
mkdir(dir2);
mkdir(dir3);
mkdir(dir4);
files = readdir(srcdir);
for i = 3:length(files)
  img = imread([srcdir '/' files{i}]);
  [H,W] = size(img);
  ar = W/H;
  W20 = ar*20;
  if W20 <= 22 
    img2 = imresize(img,[20 15],'cubic');
    #img2 = img;
    imwrite(img2,[dir1 '/' files{i}]);
  end
  if W20 >= 18 && W20 <= 27
    img2 = imresize(img,[20 25],'cubic');
    #img2 = img;
    imwrite(img2,[dir2 '/' files{i}]);
  end
  if W20 >= 23 && W20 <= 37 
    img2 = imresize(img,[20 30],'cubic');
    #img2 = img;
    imwrite(img2,[dir3 '/' files{i}]);
  end
  if W20 >= 33
    img2 = imresize(img,[20 40],'cubic');
    #img2 = img;
    imwrite(img2,[dir4 '/' files{i}]);
  end
end