try:
  st.session_state.report = run_clienthunt(
      skills=skills,
      experience=experience,
      work_preference=", ".join(work_preference),
      location_preference=location_preference,
      budget_preference=budget_preference,
      additional_requirements=additional_requirements,
      groq_api_key=groq_api_key,
  )
  st.success("Search completed!")
except Exception as error:
  st.error("Something went wrong while running the agent.")
  st.exception(error)

if "report" in st.session_state and st.session_state.report:
  st.subheader("ClientHunt Report")
  st.markdown(st.session_state.report)

  st.download_button(
      label="Download Report",
      data=st.session_state.report,
      file_name="clienthunt_report.txt",
      mime="text/plain",
  )
