clc;
clear;
close all;

%% Step 1: Read Image
img = imread('hand1.jpeg');
img = imresize(img,[512 512]);

figure; imshow(img); title('Original');

%% Step 2: Convert to Grayscale
gray = rgb2gray(img);

%% Step 3: Improve Contrast (Very Important)
enhanced = adapthisteq(gray,'ClipLimit',0.03);

figure; imshow(enhanced); title('Contrast Enhanced');

%% Step 4: Bottom-Hat Filtering (Highlights Dark Veins)
se1 = strel('disk',8);
bottomHat = imbothat(enhanced,se1);

figure; imshow(bottomHat,[]); title('Bottom-Hat Result');

%% Step 5: Further Enhance
bottomHat = imadjust(bottomHat);

%% Step 6: Threshold
level = graythresh(bottomHat);
binary = imbinarize(bottomHat,level);

binary = bwareaopen(binary,50);

figure; imshow(binary); title('Binary Veins');

%% Step 7: Skeletonization
skeleton = bwmorph(binary,'skel',Inf);

figure; imshow(skeleton); title('Skeleton');

%% Step 8: Distance Transform (Thickness Map)
distMap = bwdist(~binary);

%% Step 9: Score Veins
[y,x] = find(skeleton);

if isempty(x)
    disp('Veins not detected clearly. Try better lighting.');
    return;
end

scores = zeros(length(x),1);

for i = 1:length(x)
    scores(i) = distMap(y(i),x(i));
end

[~,idx] = max(scores);

best_x = x(idx);
best_y = y(idx);

%% Step 10: Display Final Result
figure;
imshow(img);
hold on;
plot(best_x,best_y,'ro','MarkerSize',15,'LineWidth',3);
title('Best Vein Location');
