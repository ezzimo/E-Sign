import React, { useState } from "react";
import {
  Button,
  Container,
  FormControl,
  FormLabel,
  Input,
  VStack,
  useToast,
  Heading,
  Checkbox,
} from "@chakra-ui/react";
import { SignatureRequestCreate } from "../../client/models/SignatureRequestCreate";
import { initiateSignatureRequest } from "../../client/services/SignatureRequestsService";
import Navbar from "../Common/Navbar";

const CreateSignatureRequestForm = () => {
  const [signatureRequest, setSignatureRequest] = useState<SignatureRequestCreate>({
    name: "",
    delivery_mode: "",
    ordered_signers: false,
    reminder_settings: {
      interval_in_days: 0,
      max_occurrences: 0,
      timezone: "",
    },
    expiration_date: "",
    message: "",
    expiry_date: "",
    signatories: [],
    documents: [],
  });
  const toast = useToast();

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    try {
      const response = await initiateSignatureRequest(signatureRequest);
      console.log("Request submitted successfully", response);
      toast({
        title: "Signature request created.",
        description: "The signature request has been successfully created.",
        status: "success",
        duration: 5000,
        isClosable: true,
      });
    } catch (error) {
      console.error("Error submitting signature request", error);
      toast({
        title: "Error creating signature request.",
        description: "An error occurred while creating the signature request.",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = event.target;
    setSignatureRequest(prev => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  return (
    <Container maxW="container.xl">
  		<Navbar type={"Item"} />
      <Heading size="lg" mt={5}>Create New Signature Request</Heading>
      <form onSubmit={handleSubmit}>
        <VStack spacing={4} align="stretch">
          <FormControl>
            <FormLabel htmlFor="name">Request Name</FormLabel>
            <Input id="name" name="name" value={signatureRequest.name} onChange={handleInputChange} />
          </FormControl>
          <FormControl>
            <FormLabel htmlFor="delivery_mode">Delivery Mode</FormLabel>
            <Input id="delivery_mode" name="delivery_mode" value={signatureRequest.delivery_mode} onChange={handleInputChange} />
          </FormControl>
          <FormControl>
            <FormLabel htmlFor="expiration_date">Expiration Date</FormLabel>
            <Input type="date" id="expiration_date" name="expiration_date" value={signatureRequest.expiration_date} onChange={handleInputChange} />
          </FormControl>
          <FormControl>
            <Checkbox id="ordered_signers" name="ordered_signers" isChecked={signatureRequest.ordered_signers} onChange={handleInputChange}>
              Ordered Signers
            </Checkbox>
          </FormControl>
          {/* Add more fields as per the model */}
          <Button type="submit" colorScheme="blue">Submit</Button>
        </VStack>
      </form>
    </Container>
  );
};

export default CreateSignatureRequestForm;
