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

    <div class="block">
      <el-cascader
        placeholder="处理策略"
        v-model="value"
        :options="options"
        :props="{ expandTrigger: 'hover'}"
        :clearable=true
        @change="handleChange"></el-cascader>
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
        value: [],
        options: [
          {
            value: 'ziyuan',
            label: '资源'
          },
          {
            value: 'color',
            label: '着色',
            children: [
              {
                value: 'font',
                label: '文本',
                children: [
                  {
                    value: 'red',
                    label: '红色',
                  }, {
                    value: 'blue',
                    label: '蓝色',
                  }
                ]
              },
              {
                value: 'background',
                label: '背景',
                children: [
                  {
                    value: 'red',
                    label: '红色',
                  }, {
                    value: 'blue',
                    label: '蓝色',
                  }
                ]
              }
            ]
          }
        ],


        action: '/api/hello/post',
        fileUrl: ''
      }
    },
    methods: {
      handleChange(value) {
        if (value.length === 0) {
          return
        }

        console.log(value);
      },

      beforeUpload(file) {
        console.info('文件 ' + file['name'] + ' 开始本地解析...')
      },
      onSuccess(res, file, fileList) {
        if (res['code'] !== 0) {
          this.fileUrl = ''
          this.$message.error(res['msg'])
          return
        }

        this.fileUrl = 'file://' + res['data']
        this.$refs.excel.listSheetNames(res['data'])
        this.$message.success('文件 ' + file['name'] + ' 本地解析成功！')
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
