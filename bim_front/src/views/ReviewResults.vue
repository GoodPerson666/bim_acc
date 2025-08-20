<template>

<!--  <h1>666</h1>-->
  <ReviewResult :results="results" />

</template>

<script>
import ReviewResult from '@/components/ReviewResult.vue';

export default {
  components: {
    ReviewResult
  },
  props: {
    results: {
      type: Array,
      required: true
    }
  }
};
</script>