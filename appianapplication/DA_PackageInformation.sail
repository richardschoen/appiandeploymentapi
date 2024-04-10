a!localVariables(
  /* If no pa kage data, set grid contents to null */
  local!packagelist:if(a!isNullOrEmpty(rule!DA_GetDeploymentPackages(ri!appid)),null,rule!DA_GetDeploymentPackages(ri!appid)),
{
  a!cardLayout(
    contents: {
      a!sectionLayout(
        contents: {
          a!columnsLayout(
            columns: {
              a!columnLayout(
                contents: {
                  a!textField(
                    label: "Application UUID ",
                    labelPosition: "ABOVE",
                    instructions: "Look in application properties to determine the application UUID",
                    helpTooltip: "UUID from application properties",
                    value: ri!appid,
                    saveInto: ri!appid,
                    refreshAfter: "UNFOCUS",
                    validations: {}
                  )
                }
              ),
              a!columnLayout(
                contents: {}
              )
            }
          )
        }
      )
    },
    height: "AUTO",
    style: "TRANSPARENT",
    marginBelow: "STANDARD",
    showShadow: true,
    decorativeBarPosition: "TOP"
  ),
  a!cardLayout(
    contents: {
      a!gridField(
        label: "Package List",
        labelPosition: "ABOVE",
        emptyGridMessage: "No Packages Available",
        data: local!packagelist,
        columns: {
          "",
          a!gridColumn(
            label: "Name",
            sortField: local!packagelist.name,
            value: fv!row.name,
            align: "START"
          ),
          a!gridColumn(
            label: "Desc",
            sortField: local!packagelist.description,
            value: fv!row.description,
            align: "START"
          ),
          a!gridColumn(
            label: "UUID",
            sortField: local!packagelist.uuid,
            value: fv!row.uuid,
            align: "START"
          ),
          a!gridColumn(
            label: "Ticket Link",
            sortField: local!packagelist.ticketLink,
            value: fv!row.ticketLink,
            align: "START"
          )
        },
        validations: {}
      )
    },
    height: "AUTO",
    style: "TRANSPARENT",
    marginBelow: "STANDARD",
    showShadow: true,
    decorativeBarPosition: "BOTTOM"
  ),
  a!sectionLayout(
    label: "",
    contents: {}
  )
}
)
