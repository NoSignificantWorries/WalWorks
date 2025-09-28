package main

import (
	"fmt"
	"image"
	"image/jpeg"
	"os"
)

func main() {
	file, err := os.Open("/home/dmitry/Pictures/Wallpapers/wallpaper1.jpg")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	img, format, err := image.Decode(file)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Формат изображения: %s\n", format)

	bounds := img.Bounds()
	width, height := bounds.Max.X, bounds.Max.Y
	fmt.Printf("Размер: %dx%d\n", width, height)
}
