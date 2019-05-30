import React from 'react';
import Stepper from '@material-ui/core/Stepper';
import Step from '@material-ui/core/Step';
import StepLabel from '@material-ui/core/StepLabel';
import Button from '@material-ui/core/Button';
import { Typography } from '@material-ui/core';

function HorizontalStepper() {
  const [activeStep, setActiveStep] = React.useState(0);
  const steps = ['Upload style', 'Upload content'];
  const desc = ['Upload picture of which style you want to use', 'Upload picture ']
  function handleNext() {
    setActiveStep(prevActiveStep => prevActiveStep + 1);
  }

  function handleBack() {
    setActiveStep(prevActiveStep => prevActiveStep - 1);
  }

  return (
    <div>
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
      <div>
        {activeStep === steps.length ? (
          <div>End</div>
        ):(
        <div>
          <Typography>{desc[activeStep]}</Typography>
          <div>
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