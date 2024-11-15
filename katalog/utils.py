def analyze_text(text):
    # Misalnya, analisis sederhana yang memecah teks dan mencari kata-kata tertentu
    words = text.split()
    relevant_words = [word for word in words if len(word) > 5]  # Kata lebih dari 5 huruf
    return relevant_words
