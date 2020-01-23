pkg load image
clc
clear all
close all

dirname = 'Special';
mkdir(dirname);

#fonts = ['Arial';'Hind';'Kedage';'Lohit';'Nirmala';'NotoSans';'NotoSerif';'Nudi1';'Nudi5';'Tunga'];
#threshes = [192;128;128;128;128;128;128;128;128;128];
#prefixes = ['A';'H';'K';'L';'Ni';'NSa';'NSe';'Nu1_';'Nu5_';'T'];
#lineHeights = [41;55;55;53;40;41;51;55;55;54];
#offsets = [230;233;230;230;230;228;228;229;229;232];
thresh = 192;
A = imread('0/Special.png'); 
if (isrgb(A)) 
  Ag = rgb2gray(A);
else
  Ag = A;
endif
B = Ag < thresh;
X = ones(1,size(B,2));
C = imdilate(B,X);
[D, num] = bwlabel(C);
k = 0;
for i = 1:num
  E = (D == i);
  [H,W] = find(E);
  F = B(min(H):max(H),min(W):max(W));
  AgRef = Ag(min(H):max(H),min(W):max(W));
  X2 = strel("disk",3,0);
  C2 = imdilate(F,X2);
  [D2, num2] = bwlabel(C2);
  #D2 = D2t';
  for j = 1:num2
    E2 = (D2 == j);
    [H2,W2] = find(E2);
    F2 = F(min(H2):max(H2),min(W2):max(W2));
    AgRef2 = AgRef(min(H2):max(H2),min(W2):max(W2));
    [H2,W2] = find(F2);
    final = AgRef2(min(H2):max(H2),min(W2):max(W2));
    filepath = [dirname '/' sprintf('Spcl_%d%03d',floor(k/18),322+mod(k,18)) '.png'];
    k = k + 1;
    imwrite(final,filepath);
  endfor
endfor


