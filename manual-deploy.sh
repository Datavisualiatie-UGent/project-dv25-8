#!/bin/bash

npm run build

rm -rf ../manual-deploy
mkdir ../manual-deploy
cp -r dist/* ../manual-deploy
touch ../manual-deploy/.nojekyll # Add .nojekyll file
cd ../manual-deploy

git init
git remote add origin https://github.com/datavisualiatie-ugent/project-dv25-8.git
git checkout -b gh-pages
git add .
git commit -m "Manual deploy"
git push -f origin gh-pages

cd ..
rm -rf ../manual-deploy
