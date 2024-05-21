import React, { useState } from "react";
import {
  Box,
  Button,
  Container,
  Flex,
  Heading,
  Input,
  Select,
  VStack,
  Checkbox,
  Textarea,
  useToast,
} from "@chakra-ui/react";
import { SignatureRequestCreate } from "../../client/models/SignatureRequestCreate";
import { initiateSignatureRequest } from "../../client/services/SignatureRequestsService";
import StepIndicator from "../Common/StepIndicator";
import DocumentSelect from "../Common/DocumentSelect";
import SignatoryForm from "../Common/SignatoryForm";
import FieldForm from "../Common/FieldForm";

const initialRequest: SignatureRequestCreate = {
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
};

const CreateSignatureRequestWizard = () => {
  const [step, setStep] = useState(0);
  const [signatureRequest, setSignatureRequest] = useState<SignatureRequestCreate>(initialRequest);
  const toast = useToast();

  const handleNext = () => setStep((prev) => prev + 1);
  const handlePrev = () => setStep((prev) => prev - 1);
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    if (type === "checkbox") {
      setSignatureRequest((prev) => ({
        ...prev,
        [name]: (e.target as HTMLInputElement).checked,
      }));
    } else {
      setSignatureRequest((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleDocumentSelect = (documents: number[]) => {
    setSignatureRequest((prev) => ({ ...prev, documents }));
  };

  const handleSignatoriesChange = (signatories: SignatureRequestCreate["signatories"]) => {
    setSignatureRequest((prev) => ({ ...prev, signatories }));
  };

  const handleFieldsChange = (fields: SignatureRequestCreate["signatories"][0]["fields"]) => {
    const updatedSignatories = [...signatureRequest.signatories];
    if (updatedSignatories.length > 0) {
      updatedSignatories[0].fields = fields;
      setSignatureRequest((prev) => ({ ...prev, signatories: updatedSignatories }));
    }
  };

  const handleSubmit = async () => {
    try {
      await initiateSignatureRequest(signatureRequest);
      toast({
        title: "Signature request created.",
        description: "Your signature request has been created successfully.",
        status: "success",
        duration: 5000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: "Error creating signature request.",
        description: "An error occurred while creating the signature request.",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    }
  };

  return (
    <Container maxW="container.md">
      <Heading as="h1" mb={4}>
        Create Signature Request
      </Heading>
      <StepIndicator currentStep={step} steps={["Document", "Signatories", "Fields", "Review"]} />
      <Box my={4}>
        {step === 0 && (
          <DocumentSelect selectedDocuments={signatureRequest.documents} onSelect={handleDocumentSelect} />
        )}
        {step === 1 && (
          <SignatoryForm signatories={signatureRequest.signatories} onChange={handleSignatoriesChange} />
        )}
        {step === 2 && <FieldForm fields={signatureRequest.signatories[0]?.fields || []} onChange={handleFieldsChange} />}
        {step === 3 && (
          <VStack spacing={4} align="stretch">
            <Input
              type="text"
              name="name"
              value={signatureRequest.name}
              onChange={handleInputChange}
              placeholder="Request Name"
            />
            <Select name="delivery_mode" value={signatureRequest.delivery_mode} onChange={handleInputChange}>
              <option value="">Select Delivery Mode</option>
              <option value="email">Email</option>
              <option value="direct">Direct</option>
              <option value="sms">SMS</option>
            </Select>
            <Checkbox
              name="ordered_signers"
              isChecked={signatureRequest.ordered_signers}
              onChange={handleInputChange}
            >
              Ordered Signers
            </Checkbox>
            <Input
              type="datetime-local"
              name="expiration_date"
              value={signatureRequest.expiration_date}
              onChange={handleInputChange}
            />
            <Textarea
              name="message"
              value={signatureRequest.message}
              onChange={handleInputChange}
              placeholder="Message"
            />
          </VStack>
        )}
      </Box>
      <Flex justify="space-between" mt={4}>
        {step > 0 && <Button onClick={handlePrev}>Previous</Button>}
        {step < 3 && <Button onClick={handleNext}>Next</Button>}
        {step === 3 && <Button onClick={handleSubmit}>Submit</Button>}
      </Flex>
    </Container>
  );
};

export default CreateSignatureRequestWizard;
