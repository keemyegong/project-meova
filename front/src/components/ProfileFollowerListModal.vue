<template>
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title movie-category-title" id="exampleModalLabel">
          Followers
        </h1>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="modal"
          aria-label="Close"
        ></button>
      </div>
      <div class="modal-body">
        <template v-if="store.followerlist.length !== 0">
          <div v-for="follower in store.followerlist" :key="follower.pk">
            <div class="follower-card">
              <span class="follower-card-content">
                <img
                  v-if="follower.profile_photo"
                  :src="`${movieStore.API_URL}${follower.profile_photo}`"
                  class="profile_img"
                  alt="profile_img"
                />
                <img
                  class="profile_img"
                  src="@/assets/default_profile.png"
                  v-else
                  alt=""
                />
              </span>
              <span class="follower-card-user">
                |
                {{ follower.nickname ? follower.nickname : follower.username }}
              </span>
              <button
                @click="toggleFollow(follower)"
                class="delete-btn btn btn-dark"
              >
                <div class="delete-btn-value" v-if="isFollowing(follower.pk)">
                  unfollow
                </div>
                <div class="delete-btn-value" v-else>follow</div>
              </button>
            </div>
          </div>
        </template>
        <template v-else>
          <p>아직 팔로워가 없어요!</p>
        </template>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-dark" data-bs-dismiss="modal">
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useMovieStore } from "@/stores/movie";
import { useUserStore } from "@/stores/user";
import { onMounted, computed } from "vue";
const movieStore = useMovieStore();
const store = useUserStore();
const isFollowing = (followerPk) => {
  return store.userinfo.followings.includes(followerPk);
};
const toggleFollow = async (follower) => {
  store.follow(follower.username).then(() => {
    store.settings();
    store.profile(store.userinfo.username);
    store.followings(store.userinfo.username);
  }); // Follow/Unfollow 후 사용자 정보를 다시 가져옵니다.
};

onMounted(() => {
  store.followers();
});
</script>

<style scoped>
.profile_img {
  height: 100px;
  width: 100px;
  border-radius: 50%;
}

.movie-category-title {
  margin-top: 0px;
  text-align: center;
  font-size: 50px;
  font-family: "Caprasimo", serif;
  font-weight: 400;
  font-style: normal;
}
.follower-card {
  padding: 10px;
  margin: 10px;
  background-color: #f0f0f0;
  border-radius: 10px 10px 10px 10px;
}
.follower-card-user {
  margin-left: 5px;
  font-size: 13px;
  color: lightslategray;
}
.follower-card-content {
  margin: 10px;
}
.delete-btn-value {
  font-size: 11px;
}
.delete-btn {
  margin-left: 10px;
  width: 70px;
  height: 30px;
}
.modal-content {
  width: 100%;
}
</style>
