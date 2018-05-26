# Makefile for Basler pylon sample program
.PHONY: all clean

# The program to build
NAME       := Grab

# Installation directories for pylon
PYLON_ROOT ?= /opt/pylon5

# Build tools and flags
LD         := $(CXX)
CPPFLAGS   := $(shell $(PYLON_ROOT)/bin/pylon-config --cflags)
#CXXFLAGS   = #e.g., CXXFLAGS=-g -O0 for debugging
LDFLAGS    := $(shell $(PYLON_ROOT)/bin/pylon-config --libs-rpath)
LDLIBS     := $(shell $(PYLON_ROOT)/bin/pylon-config --libs)
CPPFLAGS += $(shell pkg-config --cflags opencv)
CXXFLAGS := -c -Wall $(shell pkg-config --cflags opencv)
LDFLAGS += $(shell pkg-config --libs opencv)
CXXFLAGS += $(shell pkg-config --cflags opencv)
LDLIBS += $(shell pkg-config --libs opencv)

# Rules for building
all: $(NAME)

$(NAME): $(NAME).o
	$(LD) $(LDFLAGS) -o $@ $^ $(LDLIBS)

$(NAME).o: $(NAME).cpp
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c -o $@ $<

clean:
	$(RM) $(NAME).o $(NAME)


