import {
	Box,
	Button,
	Container,
	Flex,
	FormControl,
	FormErrorMessage,
	FormLabel,
	Heading,
	Input,
	Switch,
	Textarea,
	useColorModeValue,
} from "@chakra-ui/react";
import React from "react";
import { SubmitHandler, useForm } from "react-hook-form";
import { useMutation, useQueryClient } from "react-query";
import { SignatureRequestCreate, SignatureRequestsService } from "../../client";
import useCustomToast from "../../hooks/useCustomToast";

const CreateSignatureRequestForm: React.FC = () => {
	const queryClient = useQueryClient();
	const color = useColorModeValue("inherit", "ui.white");
	const showToast = useCustomToast();

	const {
		register,
		handleSubmit,
		reset,
		getValues,
		formState: { isSubmitting, errors, isDirty },
	} = useForm<SignatureRequestCreate>({
		mode: "onBlur",
		criteriaMode: "all",
		defaultValues: {
			name: "",
			delivery_mode: "",
			ordered_signers: false,
			// require_otp: false,
			reminder_settings: {
				interval_in_days: 0,
				max_occurrences: 0,
				timezone: "",
			},
			message: "",
			expiry_date: "",
			signatories: [], // Add appropriate initial value if needed
			documents: [], // Add appropriate initial value if needed
		},
	});

	const updateInfo = async (data: SignatureRequestCreate) => {
		await SignatureRequestsService.initiateSignatureRequest({
			requestBody: data,
		});
	};

	const mutation = useMutation(updateInfo, {
		onSuccess: () => {
			showToast(
				"Success!",
				"Signature request created successfully.",
				"success",
			);
			queryClient.invalidateQueries("signatureRequests");
			reset();
		},
		onError: (error: any) => {
			const errDetail = error.body?.detail || "Unknown error occurred";
			showToast("Something went wrong.", errDetail, "error");
		},
	});

	const onSubmit: SubmitHandler<SignatureRequestCreate> = async (data) => {
		mutation.mutate(data);
	};

	const onCancel = () => {
		reset();
	};

	return (
		<Container maxW="container.md" as="form" onSubmit={handleSubmit(onSubmit)}>
			<Heading as="h1" mb={4}>
				Create Signature Request
			</Heading>
			<Box mb={4}>
				<FormControl isInvalid={!!errors.name}>
					<FormLabel htmlFor="name" color={color}>
						Name
					</FormLabel>
					<Input
						id="name"
						{...register("name", { required: "Name is required" })}
					/>
					{errors.name && (
						<FormErrorMessage>{errors.name.message}</FormErrorMessage>
					)}
				</FormControl>
			</Box>
			<Box mb={4}>
				<FormControl isInvalid={!!errors.delivery_mode}>
					<FormLabel htmlFor="delivery_mode" color={color}>
						Delivery Mode
					</FormLabel>
					<Input
						id="delivery_mode"
						{...register("delivery_mode", {
							required: "Delivery mode is required",
						})}
					/>
					{errors.delivery_mode && (
						<FormErrorMessage>{errors.delivery_mode.message}</FormErrorMessage>
					)}
				</FormControl>
			</Box>
			<Box mb={4}>
				<FormControl isInvalid={!!errors.ordered_signers}>
					<FormLabel htmlFor="ordered_signers" color={color}>
						Ordered Signers
					</FormLabel>
					<Switch id="ordered_signers" {...register("ordered_signers")} />
					{errors.ordered_signers && (
						<FormErrorMessage>
							{errors.ordered_signers.message}
						</FormErrorMessage>
					)}
				</FormControl>
			</Box>
			{/* <Box mb={4}>
        <FormControl isInvalid={!!errors.require_otp}>
          <FormLabel htmlFor="require_otp" color={color}>
            Require OTP
          </FormLabel>
          <Switch id="require_otp" {...register("require_otp")} />
          {errors.require_otp && (
            <FormErrorMessage>{errors.require_otp.message}</FormErrorMessage>
          )}
        </FormControl>
      </Box> */}
			<Box mb={4}>
				<FormControl>
					<FormLabel color={color}>Reminder Settings</FormLabel>
					<Box mb={4}>
						<FormLabel htmlFor="interval_in_days" color={color}>
							Interval in Days
						</FormLabel>
						<Input
							id="interval_in_days"
							{...register("reminder_settings.interval_in_days", {
								required: "Interval in days is required",
							})}
						/>
						{errors.reminder_settings?.interval_in_days && (
							<FormErrorMessage>
								{errors.reminder_settings.interval_in_days.message}
							</FormErrorMessage>
						)}
					</Box>
					<Box mb={4}>
						<FormLabel htmlFor="max_occurrences" color={color}>
							Max Occurrences
						</FormLabel>
						<Input
							id="max_occurrences"
							{...register("reminder_settings.max_occurrences", {
								required: "Max occurrences is required",
							})}
						/>
						{errors.reminder_settings?.max_occurrences && (
							<FormErrorMessage>
								{errors.reminder_settings.max_occurrences.message}
							</FormErrorMessage>
						)}
					</Box>
					<Box mb={4}>
						<FormLabel htmlFor="timezone" color={color}>
							Timezone
						</FormLabel>
						<Input
							id="timezone"
							{...register("reminder_settings.timezone", {
								required: "Timezone is required",
							})}
						/>
						{errors.reminder_settings?.timezone && (
							<FormErrorMessage>
								{errors.reminder_settings.timezone.message}
							</FormErrorMessage>
						)}
					</Box>
				</FormControl>
			</Box>
			<Box mb={4}>
				<FormControl isInvalid={!!errors.message}>
					<FormLabel htmlFor="message" color={color}>
						Message
					</FormLabel>
					<Textarea id="message" {...register("message")} />
					{errors.message && (
						<FormErrorMessage>{errors.message.message}</FormErrorMessage>
					)}
				</FormControl>
			</Box>
			<Box mb={4}>
				<FormControl isInvalid={!!errors.expiry_date}>
					<FormLabel htmlFor="expiry_date" color={color}>
						Expiry Date
					</FormLabel>
					<Input
						id="expiry_date"
						type="date"
						{...register("expiry_date", {
							required: "Expiry date is required",
						})}
					/>
					{errors.expiry_date && (
						<FormErrorMessage>{errors.expiry_date.message}</FormErrorMessage>
					)}
				</FormControl>
			</Box>
			<Flex mt={4} gap={3}>
				<Button
					variant="primary"
					type="submit"
					isLoading={isSubmitting}
					isDisabled={!isDirty || !getValues("name")}
				>
					Submit
				</Button>
				<Button onClick={() => onCancel()} isDisabled={isSubmitting}>
					Cancel
				</Button>
			</Flex>
		</Container>
	);
};

export default CreateSignatureRequestForm;
