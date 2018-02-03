$(function () {
    $(".posts-results li").click(function () {
      var posts = $(this).attr("post-id");
      location.href = "/posts/" + posts + "/"; //TODO change link to posts
    });
});
