import React, { ChangeEvent } from 'react';
import { FormControl, FormLabel, Input, VStack } from '@chakra-ui/react';
import { FormData } from './types';

interface StepOneProps {
  formData: FormData;
  setFormData: React.Dispatch<React.SetStateAction<FormData>>;
}

const StepOne: React.FC<StepOneProps> = ({ formData, setFormData }) => {
  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  return (
    <VStack spacing={4} align="stretch">
      <FormControl isRequired>
        <FormLabel htmlFor="name">Request Name</FormLabel>
        <Input id="name" name="name" value={formData.name || ''} onChange={handleChange} />
      </FormControl>
      <FormControl isRequired>
        <FormLabel htmlFor="deliveryMode">Delivery Mode</FormLabel>
        <Input id="deliveryMode" name="deliveryMode" value={formData.deliveryMode || ''} onChange={handleChange} />
      </FormControl>
    </VStack>
  );
};

export default StepOne;
