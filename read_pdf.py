import pymupdf

def read_pdf(path):
    doc = pymupdf.open(path)

    context = []
    for d in doc:
        content = d.get_text()
        context.append(content)

    full_text = "\n".join(context)
    return full_text

if __name__ == "__main__":
    full = read_pdf("data/product_manual.pdf")
    print(full[:300])