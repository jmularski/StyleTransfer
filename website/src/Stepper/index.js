import React from 'react';
import Stepper from '@material-ui/core/Stepper';
import Step from '@material-ui/core/Step';
import StepLabel from '@material-ui/core/StepLabel';
import Button from '@material-ui/core/Button';
import Dropper from '../FileDropper';
import { Typography } from '@material-ui/core';

function HorizontalStepper() {
  const [activeStep, setActiveStep] = React.useState(0);
  const steps = ['Upload style', 'Upload content'];
  const desc = ['Upload picture of which style you want to use', 'Upload picture on which you want to transfer this style'];
  const images = []

  function imageHandler(imageData) {
    images.push(imageData);
  };

  function sendImagesToServer() {
    //implement later
    console.log(images);
  };

  function handleNext() {
    setActiveStep(prevActiveStep => prevActiveStep + 1);
    
    if(activeStep + 1 === steps.length) {
      sendImagesToServer();
    }
  }

  function handleBack() {
    setActiveStep(prevActiveStep => prevActiveStep - 1);
  }

  return (
    <div >
      <Stepper activeStep = {activeStep}>
        {steps.map((label, index) => {
          const stepProps = {};
          const labelProps = {};

          return (
            <Step key={label} {...stepProps}>
              <StepLabel {...labelProps}>{label}</StepLabel>
            </Step>
          )
        })}
      </Stepper>
      <div style = {{ display: 'flex', justifyContent: 'center' }}>
        {activeStep === steps.length ? (
          <div>End</div>
        ):(
        <div>
          <Typography style = {{paddingBottom: '5%'}}>{desc[activeStep]}</Typography>
          <Dropper imageCallback = {imageHandler}/>
          <div style = {{ display: 'flex', justifyContent: 'center' }}>
            <Button disabled = {activeStep === 0} onClick = {handleBack}>
              Back
            </Button>

            <Button
              variant="contained"
              color="primary"
              onClick={handleNext}
            >
              { activeStep === steps.length - 1 ? "Finish" : "Next"}
            </Button>
          </div>
        </div>
        )}
      </div>
    </div>
  )
}

export default HorizontalStepper;