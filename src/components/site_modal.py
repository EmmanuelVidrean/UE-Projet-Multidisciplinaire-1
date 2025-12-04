import dash_bootstrap_components as dbc


def site_modal():
    """
    Modal pour afficher les infos d'un site UNESCO.
    IDs fixes :
      - id="site-modal"
      - title: id="modal-title"
      - body: id="modal-body"
    """
    return dbc.Modal(
        id="site-modal",
        size="lg",
        is_open=False,
        children=[
            dbc.ModalHeader(dbc.ModalTitle(id="modal-title")),
            dbc.ModalBody(id="modal-body"),
        ],
    )
