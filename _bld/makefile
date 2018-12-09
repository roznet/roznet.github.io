POST_DIR=../_posts
IMG_DIR=../assets/clouds

POST_FILES=$(shell find $(POST_DIR) -type f -name *.md)
IMG_FILES=$(patsubst $(POST_DIR)/%,$(IMG_DIR)/%,$(POST_FILES:.md=.png))

all: $(IMG_FILES)

clean:
	rm $(IMG_FILES)

$(IMG_DIR)/%.png: $(POST_DIR)/%.md
	./gencloud.py -o $(IMG_DIR) $<
