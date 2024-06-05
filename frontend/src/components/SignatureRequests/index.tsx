import { useState } from "react";
import { Container, Heading, Button } from '@chakra-ui/react';
import StepOne from './StepOne';
import StepTwo from './StepTwo';
import StepThree from './StepThree';
import { FormData } from './types';

const initialFormData: FormData = {
  name: '',
  deliveryMode: '',
  orderedSigners: false,
  reminderSettings: {
    intervalInDays: 0,
    maxOccurrences: 0,
    timezone: 'Europe/Paris',
  },
  expirationDate: '',
  message: '',
};

const CreateSignatureRequest = () => {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState(initialFormData);

  const nextStep = () => setStep(step + 1);
  const prevStep = () => setStep(step - 1);

  const handleSubmit = () => {
    console.log('Submitting Data:', formData);
  };

  const renderStep = () => {
    switch (step) {
      case 1:
        return <StepOne formData={formData} setFormData={setFormData} />;
      case 2:
        return <StepTwo formData={formData} setFormData={setFormData} />;
      case 3:
        return <StepThree formData={formData} onSubmit={handleSubmit} />;
      default:
        return <StepOne formData={formData} setFormData={setFormData} />;
    }
  };

  return (
    <Container maxW="container.xl">
      <Heading size="lg" mt={5}>Create New Signature Request</Heading>
      {renderStep()}
      {step > 1 && <Button onClick={prevStep}>Back</Button>}
      {step < 3 && <Button onClick={nextStep}>Next</Button>}
    </Container>
  );
};

export default CreateSignatureRequest;
