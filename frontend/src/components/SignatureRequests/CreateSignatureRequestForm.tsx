import React, { useState } from 'react';
import {
  Button,
  Container,
  FormControl,
  FormLabel,
  Input,
  VStack,
  Textarea,
  Checkbox,
  useToast,
  Heading,
} from '@chakra-ui/react';
import { useMutation } from 'react-query';
import Navbar from '../Common/Navbar';


// Define your type for the form data
interface SignatureRequestFormData {
  name: string;
  deliveryMode: string;
  orderedSigners: boolean;
  reminderSettings: {
    intervalInDays: number;
    maxOccurrences: number;
    timezone: string;
  };
  expirationDate: string;
  message: string;
}

const CreateSignatureRequestForm = () => {
  const toast = useToast();
  const [formData, setFormData] = useState({
    name: '',
    deliveryMode: 'email',
    orderedSigners: false,
    reminderSettings: {
      intervalInDays: 3,
      maxOccurrences: 5,
      timezone: 'Europe/Paris',
    },
    expirationDate: '',
    message: '',
  });

  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const target = e.target as HTMLInputElement;  // Typecasting to HTMLInputElement to access 'checked'
    const { name, value, type, checked } = target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  // Placeholder function for submission
  const { mutate: submitSignatureRequest } = useMutation(
    async (data: SignatureRequestFormData) => {
      setIsLoading(true);  // Set loading to true at start of submission
      console.log(data); // For debugging, here you'd usually make an API call
      // Simulate a network request
      await new Promise(resolve => setTimeout(resolve, 2000));
      setIsLoading(false);  // Reset loading state after request is complete
    },
    {
      onSuccess: () => {
        toast({
          title: 'Request created.',
          description: 'The signature request has been successfully created.',
          status: 'success',
          duration: 9000,
          isClosable: true,
        });
      },
      onError: (error: any) => {
        toast({
          title: 'Error creating request.',
          description: 'An error occurred while creating the signature request: ' + error.message,
          status: 'error',
          duration: 9000,
          isClosable: true,
        });
        console.error('Error submitting signature request', error);
        setIsLoading(false);  // Ensure loading state is reset on error
      },
    }
  );

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    submitSignatureRequest(formData);
  };

  return (
    <Container maxW="container.xl">
      <Navbar type="Document" />
      <Heading size="lg" mt={5}>Create New Signature Request</Heading>
      <form onSubmit={handleSubmit}>
        <VStack spacing={4} align="stretch">
          <FormControl isRequired>
            <FormLabel htmlFor="name">Request Name</FormLabel>
            <Input id="name" name="name" value={formData.name} onChange={handleChange} />
          </FormControl>
          <FormControl isRequired>
            <FormLabel htmlFor="expirationDate">Expiration Date</FormLabel>
            <Input type="date" id="expirationDate" name="expirationDate" value={formData.expirationDate} onChange={handleChange} />
          </FormControl>
          <FormControl>
            <FormLabel htmlFor="message">Message</FormLabel>
            <Textarea id="message" name="message" value={formData.message} onChange={handleChange} />
          </FormControl>
          <FormControl>
            <Checkbox id="orderedSigners" name="orderedSigners" isChecked={formData.orderedSigners} onChange={handleChange}>
              Ordered Signers
            </Checkbox>
          </FormControl>
          <Button type="submit" colorScheme="blue" isLoading={isLoading}>Submit</Button>
        </VStack>
      </form>
    </Container>
  );
};

export default CreateSignatureRequestForm;
