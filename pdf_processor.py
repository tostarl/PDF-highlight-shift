import fitz  # PyMuPDF

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return tuple(c / 255.0 for c in rgb)


def replace_highlight_colors_hex(input_pdf, output_pdf, color_mapping, tolerance=0.1):
    color_mapping_rgb = {
        tuple(round(c, 2) for c in hex_to_rgb(old_hex)): hex_to_rgb(new_hex)
        for old_hex, new_hex in color_mapping.items()
    }

    doc = fitz.open(input_pdf)
    for page in doc:
        annotations = page.annots()
        if annotations:
            for annot in annotations:
                if annot.type[0] == 8:  # 高亮注释
                    color = annot.colors.get("stroke", None)
                    if color:
                        color_tuple = tuple(round(c, 2) for c in color)
                        matched = False
                        for mapped_color, new_color in color_mapping_rgb.items():
                            if all(abs(color_tuple[i] - mapped_color[i]) <= tolerance for i in range(3)):
                                annot.set_colors(stroke=new_color)
                                annot.update()
                                matched = True
                                break  # 找到匹配的颜色后，跳出循环
                        if not matched:
                            print(f"Could not match color: {color_tuple} on page {page.number}")
    doc.save(output_pdf)
    doc.close()
