for file in package/ui/Widgets/ui/*; do
  	pyuic5 "$file" -o "package/ui/Widgets/generated/$(basename "$file" .ui)_.py"
done