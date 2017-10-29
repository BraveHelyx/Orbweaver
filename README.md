# Orbweaver

![Orbweaver](https://github.com/BraveHelyx/Orbweaver/blob/master/img/orbweaver.png)

## Description
Orbweaver is a directed web spider designed to assist a forensic investigation of a website or web application. It is discrete, prioritising making fewer requests in order to generate a surface area of interesting targets.

## Usage
python orbweaver.py http://www.example.com

## Known Issues
There is an issue saving sessions which have queried URLs where one is a subset of another.