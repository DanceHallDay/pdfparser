g++ -O3 -Wall -shared -fPIC $(python3.10-config --includes) $(python3.10 -m pybind11 --includes) -o pdfparser/pdf2text$(python3.10-config --extension-suffix) pdfparser/cpp/pdf2text.cpp -L. poppler/libpoppler-cpp.so 