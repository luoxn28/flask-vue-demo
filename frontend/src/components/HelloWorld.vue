<template>
  <div class="hello">
    <el-upload class="upload-demo" drag action='' :action=action :show-file-list=false
               :before-upload=beforeUpload :on-success=onSuccess :on-error=onError>
      <i class="el-icon-upload"></i>
      <div class="el-upload__text">将excel文件拖到此处，或<em>点击上传</em></div>
    </el-upload>

    <div v-if="fileUrl !== ''">
      <el-link type="success" :href="fileUrl">{{fileUrl}}</el-link>
    </div>

    <Excel ref="excel"></Excel>
  </div>
</template>

<script>
  import Excel from "./Excel";

  export default {
    name: 'HelloWorld',
    components: {Excel},
    data() {
      return {
        action: '/api/hello/post',
        fileUrl: ''
      }
    },
    methods: {
      beforeUpload(file) {
        console.info('文件 ' + file['name'] + ' 开始本地解析...')
      },
      onSuccess(res, file, fileList) {
        if (res['code'] !== 0) {
          this.fileUrl = ''
          this.$message.error('文件 ' + file['name'] + ' 本地解析发生错误：' + res['data'])
          return
        }

        this.$message.success('文件 ' + file['name'] + ' 本地解析成功！')
        this.fileUrl = 'file://' + res['data']
        this.$refs.excel.listSheetNames(res['data'])
      },
      onError(err, file, fileList) {
        this.$message.error('文件 ' + file['name'] + ' 本地解析发生错误：' + err)
        this.fileUrl = ''
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
