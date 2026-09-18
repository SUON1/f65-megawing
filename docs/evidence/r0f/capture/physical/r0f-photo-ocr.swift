import Foundation
import Vision
import AppKit

for path in CommandLine.arguments.dropFirst() {
    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.usesLanguageCorrection = false
    let handler = VNImageRequestHandler(url: URL(fileURLWithPath: path))
    try handler.perform([request])
    let lines = (request.results ?? []).map { observation -> [String: Any] in
        let box = observation.boundingBox
        return ["text": observation.topCandidates(1).first?.string ?? "", "x": box.minX, "y": box.minY, "w": box.width, "h": box.height]
    }
    let json = try JSONSerialization.data(withJSONObject: ["path": path, "lines": lines], options: [.sortedKeys])
    print(String(data: json, encoding: .utf8)!)
}
