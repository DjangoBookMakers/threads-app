document.addEventListener("DOMContentLoaded", function () {
  // 부트스트랩 툴팁 초기화
  const tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]'),
  );
  const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // 자동으로 텍스트 영역 높이 조절
  const autoResizeTextareas = document.querySelectorAll(".auto-resize");
  autoResizeTextareas.forEach((textarea) => {
    textarea.addEventListener("input", function () {
      this.style.height = "auto";
      this.style.height = this.scrollHeight + "px";
    });

    // 초기 로드 시에도 높이 조절
    textarea.dispatchEvent(new Event("input"));
  });

  // 알림 메시지 자동 닫힘 설정
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach((alert) => {
    setTimeout(() => {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 5000); // 5초 후 자동 닫힘
  });

  // 다크 모드 토글 (로컬 스토리지 사용)
  const darkModeToggle = document.getElementById("dark-mode-toggle");

  if (darkModeToggle) {
    // 저장된 테마 설정 확인
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
      document.body.classList.add("dark-mode");
      darkModeToggle.checked = true;
    }

    // 테마 변경 이벤트
    darkModeToggle.addEventListener("change", function () {
      if (this.checked) {
        document.body.classList.add("dark-mode");
        localStorage.setItem("theme", "dark");
      } else {
        document.body.classList.remove("dark-mode");
        localStorage.setItem("theme", "light");
      }
    });
  }

  // 이미지 미리보기 기능
  const imageInputs = document.querySelectorAll(".image-upload");
  imageInputs.forEach((input) => {
    input.addEventListener("change", function () {
      const previewContainer = document.querySelector(this.dataset.preview);
      if (previewContainer) {
        previewContainer.innerHTML = "";

        if (this.files && this.files[0]) {
          const reader = new FileReader();
          reader.onload = function (e) {
            const img = document.createElement("img");
            img.src = e.target.result;
            img.className = "img-thumbnail mt-2";
            img.style.maxHeight = "200px";
            previewContainer.appendChild(img);

            // 취소 버튼 추가
            const cancelBtn = document.createElement("button");
            cancelBtn.type = "button";
            cancelBtn.className = "btn btn-sm btn-danger mt-1";
            cancelBtn.textContent = "취소";
            cancelBtn.addEventListener("click", function () {
              input.value = "";
              previewContainer.innerHTML = "";
            });
            previewContainer.appendChild(cancelBtn);
          };
          reader.readAsDataURL(this.files[0]);
        }
      }
    });
  });
});

// CSRF 토큰 가져오기 (AJAX 요청용)
function getCsrfToken() {
  return document.querySelector("[name=csrfmiddlewaretoken]").value;
}

// 문자열 길이 제한 헬퍼 함수
function truncateText(text, maxLength) {
  if (text.length <= maxLength) return text;
  return text.substr(0, maxLength) + "...";
}

// 날짜 포맷팅 함수
function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString("ko-KR", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}
