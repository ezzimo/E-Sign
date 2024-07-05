import {
	Container,
	Heading,
	Tab,
	TabList,
	TabPanel,
	TabPanels,
	Tabs,
} from "@chakra-ui/react";
import { createFileRoute } from "@tanstack/react-router";
import { useQueryClient } from "react-query";

import type { UserOut } from "../../client";
import CreateSignatureRequestForm from "../../components/SignatureRequests/CreateSignatureRequestForm";
import UserInformation from "../../components/UserSettings/UserInformation";
// import { createRoute } from '@tanstack/react-router';
// import { Route as LayoutRoute } from "../_layout";

// export const Route = createRoute({
//   getParentRoute: () => LayoutRoute,
//   path: "/new_signature_requests",
//   component: CreateSignatureRequestForm,
// });

const tabsConfig = [
	{ title: "My profile", component: UserInformation },
	{ title: "Signature Request", component: CreateSignatureRequestForm },
];

export const Route = createFileRoute("/_layout/create_signature_request")({
	component: SignatureSettings,
});

function SignatureSettings() {
	const queryClient = useQueryClient();
	const currentUser = queryClient.getQueryData<UserOut>("currentUser");
	const finalTabs = currentUser?.is_superuser
		? tabsConfig.slice(0, 3)
		: tabsConfig;

	return (
		<Container maxW="full">
			<Heading size="lg" textAlign={{ base: "center", md: "left" }} py={12}>
				Signature Settings
			</Heading>
			<Tabs variant="enclosed">
				<TabList>
					{finalTabs.map((tab, index) => (
						<Tab key={index}>{tab.title}</Tab>
					))}
				</TabList>
				<TabPanels>
					{finalTabs.map((tab, index) => (
						<TabPanel key={index}>
							<tab.component />
						</TabPanel>
					))}
				</TabPanels>
			</Tabs>
		</Container>
	);
}

export default SignatureSettings;
