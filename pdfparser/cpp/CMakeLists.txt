cmake_minimum_required(VERSION 3.23)
project(parser)

set(CMAKE_CXX_STANDARD 14)

add_library(poppler SHARED IMPORTED)
set_target_properties(poppler PROPERTIES
  IMPORTED_LOCATION "${CMAKE_SOURCE_DIR}/poppler/libpoppler-cpp.so"
  INTERFACE_INCLUDE_DIRECTORIES "${CMAKE_SOURCE_DIR}/poppler/cpp"
)

add_subdirectory(pybind11)
pybind11_add_module(pdf2text pdf2text.cpp)
target_link_libraries(pdf2text PRIVATE poppler)
