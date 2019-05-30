import React from 'react';
import Dropzone from 'react-dropzone';

export default class Dropper extends React.Component {
  constructor(props) {
    super(props);

    this.parseImg = this.parseImg.bind(this);
  }

  parseImg(image) {
    console.log(image);
    const reader = new FileReader();

    reader.onload = () => {
      this.props.imageCallback(reader.result)
    }

    reader.readAsDataURL(image);
  }

  render() {
    return (
      <Dropzone onDrop={acceptedFiles => this.parseImg(acceptedFiles[0])}>
        {({getRootProps, getInputProps}) => (
          <section>
            <div {...getRootProps()} style = {{padding: '2%', marginBottom: '5%', borderStyle: 'dashed', borderColor: 'grey', borderWidth: 'thin' }}>
              <input {...getInputProps()} />
              <p>Drag 'n' drop some files here, or click to select files</p>
            </div>
          </section>
        )}
      </Dropzone>
    )
  }
}