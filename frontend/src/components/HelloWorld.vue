<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <h2>Essential Links</h2>

    <el-input type="textarea" :rows="2" placeholder="请输入内容" v-model="textarea"></el-input>
    <el-row>
      <el-button type="primary" @click="onSubmit" round>获取结果</el-button>
    </el-row>
    <el-row>
      <p>{{ response }}</p>
    </el-row>
  </div>
</template>

<script>
  export default {
    name: 'HelloWorld',
    data() {
      return {
        msg: 'Welcome to Your Vue.js App',
        textarea: '',
        response: ''
      }
    },
    methods: {
      onSubmit() {
        this.axios.post("/hello/world", {
          "word": this.textarea
        }).then(
          res => {
            console.log(res.data)
            this.response = res.data
          }
        ).catch(res => {
          console.log(res.data.res)
        })
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  h1, h2 {
    font-weight: normal;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    display: inline-block;
    margin: 0 10px;
  }

  a {
    color: #42b983;
  }
</style>
