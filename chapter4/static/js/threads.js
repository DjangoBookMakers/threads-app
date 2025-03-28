document.addEventListener("DOMContentLoaded", function () {
  // 좋아요 버튼 이벤트 리스너
  const likeButtons = document.querySelectorAll(".like-button");
  likeButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const threadId = this.getAttribute("data-thread-id");
      const likeIcon = this.querySelector("i");
      const likeCount = this.querySelector(".like-count");

      // UI 상태 미리 업데이트 (나중에 실제 연동 시 AJAX 사용)
      if (likeIcon.classList.contains("far")) {
        likeIcon.classList.remove("far");
        likeIcon.classList.add("fas");
        likeCount.textContent = parseInt(likeCount.textContent) + 1;
      } else {
        likeIcon.classList.remove("fas");
        likeIcon.classList.add("far");
        likeCount.textContent = parseInt(likeCount.textContent) - 1;
      }

      // 추후 AJAX 호출로 서버에 좋아요 상태 업데이트
      // 현재는 UI 데모만 구현
    });
  });

  // 댓글 버튼 이벤트 리스너
  const commentButtons = document.querySelectorAll(".comment-button");
  commentButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const threadId = this.getAttribute("data-thread-id");
      const commentForm = document.querySelector(`#comment-form-${threadId}`);

      if (commentForm) {
        // 댓글 폼 토글
        if (commentForm.style.display === "none") {
          commentForm.style.display = "block";
          commentForm.querySelector("textarea").focus();
        } else {
          commentForm.style.display = "none";
        }
      }
    });
  });

  // 공유 버튼 이벤트 리스너
  const shareButtons = document.querySelectorAll(".share-button");
  shareButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const threadId = this.getAttribute("data-thread-id");
      const threadUrl = `${window.location.origin}/thread/${threadId}/`;

      // 웹 공유 API 지원 확인
      if (navigator.share) {
        navigator
          .share({
            title: "Threads에서 공유된 게시물",
            url: threadUrl,
          })
          .catch(console.error);
      } else {
        // 클립보드에 URL 복사 (폴백)
        const tempInput = document.createElement("input");
        document.body.appendChild(tempInput);
        tempInput.value = threadUrl;
        tempInput.select();
        document.execCommand("copy");
        document.body.removeChild(tempInput);

        // 사용자에게 알림
        alert("링크가 클립보드에 복사되었습니다.");
      }
    });
  });

  // 스레드 작성 폼 문자 수 카운터
  const threadTextareas = document.querySelectorAll(".thread-textarea");
  threadTextareas.forEach((textarea) => {
    const counter = document.querySelector(`#thread-content-counter`);

    if (counter) {
      const maxLength = 500; // 최대 글자 수 (500자)

      textarea.addEventListener("input", function () {
        const remainingChars = maxLength - this.value.length;
        counter.textContent = remainingChars;

        // 글자 수에 따른 스타일 변경
        if (remainingChars < 0) {
          counter.classList.add("text-danger");
          counter.classList.remove("text-muted", "text-warning");
        } else if (remainingChars < 20) {
          counter.classList.add("text-warning");
          counter.classList.remove("text-muted", "text-danger");
        } else {
          counter.classList.add("text-muted");
          counter.classList.remove("text-warning", "text-danger");
        }
      });

      // 초기 카운터 값 설정
      textarea.dispatchEvent(new Event("input"));
    }
  });
});

// 스레드 삭제 확인
function confirmDeleteThread(threadId) {
  if (confirm("정말로 이 스레드를 삭제하시겠습니까?")) {
    window.location.href = `/thread/${threadId}/delete/`;
  }
}

// 스레드 더 보기 로드 (무한 스크롤용)
function loadMoreThreads() {
  const loadMoreButton = document.querySelector("#load-more-button");
  if (loadMoreButton) {
    loadMoreButton.innerHTML =
      '<span class="spinner-border spinner-border-sm"></span> 로딩 중...';
    loadMoreButton.disabled = true;

    // 실제 구현에서는 AJAX 요청으로 추가 스레드 로딩
    // 현재는 UI 데모만 구현
    setTimeout(() => {
      loadMoreButton.innerHTML = "더 보기";
      loadMoreButton.disabled = false;
    }, 1500);
  }
}

// 댓글 삭제 확인
function confirmDeleteComment(commentId) {
  if (confirm("정말로 이 댓글을 삭제하시겠습니까?")) {
    // AJAX 요청으로 댓글 삭제
    fetch(`/comment/${commentId}/delete/`, {
      method: "POST",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCsrfToken(),
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          // 댓글 요소 제거
          const commentElement = document.querySelector(
            `#comment-${commentId}`,
          );
          if (commentElement) {
            commentElement.remove();

            // 댓글 카운트 업데이트
            const threadId = commentElement
              .closest(".thread-card")
              ?.id.replace("thread-", "");
            if (threadId) {
              const countElement = document.querySelector(
                `button.comment-button[data-thread-id="${threadId}"] span`,
              );
              if (countElement) {
                countElement.textContent =
                  parseInt(countElement.textContent) - 1;
              }
            }
          }
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
}

// 빠른 댓글 폼 제출 (AJAX)
document.addEventListener("DOMContentLoaded", function () {
  const quickCommentForms = document.querySelectorAll(".quick-comment-form");

  quickCommentForms.forEach((form) => {
    form.addEventListener("submit", function (e) {
      e.preventDefault();

      const threadId = this.action.match(/thread\/(\d+)\/comment/)[1];
      const textarea = this.querySelector("textarea");
      const content = textarea.value.trim();

      if (!content) return;

      fetch(this.action, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": getCsrfToken(),
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `content=${encodeURIComponent(content)}`,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "success") {
            // 댓글 폼 초기화
            textarea.value = "";

            // 댓글 카운트 업데이트
            const countElement = document.querySelector(
              `button.comment-button[data-thread-id="${threadId}"] span`,
            );
            if (countElement) {
              countElement.textContent = parseInt(countElement.textContent) + 1;
            }

            // 성공 메시지 표시
            alert("댓글이 작성되었습니다.");

            // 댓글 폼 닫기
            const commentForm = document.querySelector(
              `#comment-form-${threadId}`,
            );
            if (commentForm) {
              commentForm.style.display = "none";
            }
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    });
  });
});
