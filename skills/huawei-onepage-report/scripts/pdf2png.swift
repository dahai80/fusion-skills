import PDFKit; import AppKit
let d = PDFDocument(url: URL(fileURLWithPath: CommandLine.arguments[1]))!
print("pages", d.pageCount)
for i in 0..<d.pageCount { let p = d.page(at: i)!; let b = p.bounds(for: .mediaBox)
 let img = p.thumbnail(of: NSSize(width: b.width*1.6, height: b.height*1.6), for: .mediaBox)
 let rep = NSBitmapImageRep(data: img.tiffRepresentation!)!
 try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: CommandLine.arguments[2] + "/p\(i+1).png")) }
