import os
from gtts import gTTS
from moviepy.editor import AudioFileClip

# -----------------------------
# Nội dung cần chuyển thành giọng nói
# -----------------------------
text = """
Xin chào các bạn.
Hôm nay, tôi muốn chia sẻ đôi điều về tầm quan trọng của việc quản lý thời gian trong học tập và cuộc sống. Thời gian là một nguồn tài nguyên vô giá mà mỗi người đều có như nhau: 24 giờ trong một ngày, 7 ngày trong một tuần. Điểm khác biệt nằm ở cách chúng ta sử dụng quỹ thời gian ấy.

Trong học tập, nếu biết sắp xếp thời gian hợp lý, chúng ta có thể hoàn thành bài tập đúng hạn, ôn luyện kiến thức hiệu quả và vẫn dành được khoảng trống cho việc nghỉ ngơi, giải trí. Ngược lại, nếu lãng phí thời gian vào những việc không cần thiết, chúng ta sẽ luôn cảm thấy bị cuốn theo áp lực, dễ rơi vào trạng thái mệt mỏi và căng thẳng.

Quản lý thời gian không chỉ là lên kế hoạch, mà còn là khả năng kiên trì thực hiện kế hoạch đó. Bạn có thể bắt đầu bằng những việc đơn giản như viết ra danh sách công việc cần làm mỗi ngày, ưu tiên những việc quan trọng, và dành thời gian cố định cho học tập cũng như nghỉ ngơi.

Ngoài ra, việc biết nói “không” với những yếu tố gây xao nhãng, như mạng xã hội hay trò chơi trực tuyến, cũng là một phần quan trọng trong quản lý thời gian. Khi bạn biết kiểm soát bản thân, bạn sẽ thấy mình có nhiều thời gian hơn để học tập, rèn luyện kỹ năng và phát triển bản thân.

Cuối cùng, hãy nhớ rằng, quản lý thời gian tốt không chỉ giúp chúng ta học tập hiệu quả hơn, mà còn tạo nên sự cân bằng trong cuộc sống. Một người biết sắp xếp thời gian hợp lý sẽ có nhiều cơ hội để thành công và hạnh phúc hơn trong tương lai.

Xin cảm ơn các bạn đã lắng nghe.
"""

# -----------------------------
# Bước 1: Tạo file MP3 từ gTTS
# -----------------------------
file_mp3 = "ghi_am_quan_ly_thoi_gian.mp3"
file_wav = "ghi_am_quan_ly_thoi_gian.wav"

tts = gTTS(text=text, lang="vi")
tts.save(file_mp3)
print(f"✅ Đã tạo file MP3: {file_mp3}")

# -----------------------------
# Bước 2: Chuyển MP3 sang WAV bằng moviepy
# -----------------------------
if os.path.exists(file_mp3):
    audio = AudioFileClip(file_mp3)
    audio.write_audiofile(file_wav)
    print(f"✅ Đã chuyển sang WAV: {file_wav}")
else:
    print(f"❌ Không tìm thấy file MP3: {file_mp3}")
