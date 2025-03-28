document.addEventListener("DOMContentLoaded", function () {
  // 팔로우 버튼 이벤트 리스너
  const followButtons = document.querySelectorAll(".follow-button");
  followButtons.forEach((button) => {
    button.addEventListener("click", function () {
      if (!isAuthenticated) {
        // 로그인 필요 알림
        alert("팔로우하려면 로그인이 필요합니다.");
        return;
      }

      const username = this.getAttribute("data-username");

      // AJAX 요청으로 팔로우 상태 업데이트
      fetch(`/accounts/follow/${username}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCsrfToken(),
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "success") {
            // UI 업데이트
            if (data.is_following) {
              this.textContent = "언팔로우";
            } else {
              this.textContent = "팔로우";
            }

            // 팔로워/팔로잉 수 업데이트
            const followersCount = document.querySelector(".followers-count");
            const followingCount = document.querySelector(".following-count");

            if (followersCount) {
              followersCount.textContent = data.followers_count;
            }
            if (followingCount) {
              followingCount.textContent = data.following_count;
            }
          } else {
            alert(data.message || "오류가 발생했습니다.");
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    });
  });
});
