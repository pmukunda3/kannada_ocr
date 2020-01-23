pkg load image
more off
clc
clear all
close all

dirname = 'Samples_NEW';
mkdir(dirname);

fonts = ['Arial';'Hind';'Kedage';'Lohit';'Nirmala';'NotoSans';'NotoSerif';'Nudi1';'Nudi5';'Tunga'];
threshes = [192;128;128;128;128;128;128;128;128;128];
prefixes = ['A';'H';'K';'L';'Ni';'NSa';'NSe';'Nu1_';'Nu5_';'T'];
lineHeights = [41;55;55;53;40;41;51;55;55;54];
offsets = [230;233;230;230;230;228;228;229;229;232];

for j = 1:10
font = strtrim(fonts(j,:));
thresh = threshes(j);
prefix = strtrim(prefixes(j,:));
lineHeight = lineHeights(j);
offset = offsets(j);  
name = font;
A = imread(['0/' name '.png']); 
if (isrgb(A)) 
  Ag = rgb2gray(A);
else
  Ag = A;
endif
B = Ag < thresh;
if j == 4
X = strel("disk",2,0);
else
X = strel("disk",3,0);
endif
%C = B;
C = imdilate(B,X);
%imshow(C);
[D, num] = bwlabel(C);
Pts = [];
for i = 1:num
  E = (D == i);
  [H,W] = find(E);
  F = B(min(H):max(H),min(W):max(W));
  %[H,W] = find(F);
  HRnd = lineHeight*floor((max(H)-offset)/lineHeight)+offset;
  Pts = [Pts;[i HRnd min(W)]];
endfor
Pts = sortrows(Pts,[2,3]);
for i = 1:num
  E = (D == Pts(i,1));
  [H,W] = find(E);
  F = Ag(min(H):max(H),min(W):max(W));
  G = F < thresh;
  [H,W] = find(G);
  final = F(min(H):max(H),min(W):max(W));
  #G = 1 - G;
  #final = G > 0.5;
  #final = imresize(G,[40 NaN],'linear') > 0.5;
  classes = num/2;
  if i > classes  
  filepath = [dirname '/' prefix 'b' sprintf('%03d',i-1-classes) '.png'];
  else
  filepath = [dirname '/' prefix sprintf('%03d',i-1) '.png'];
  endif
  imwrite(final,filepath);
endfor
endfor

