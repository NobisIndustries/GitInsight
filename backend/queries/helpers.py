import db_schema


def get_common_query_init_arguments():  # Because I am to lazy to import these things everytime in the endpoints
    from queries.info_providers import AuthorInfoProvider, BranchInfoProvider

    db_session = db_schema.get_session()
    author_info_provider = AuthorInfoProvider()
    branch_info_provider = BranchInfoProvider()
    return db_session, author_info_provider, branch_info_provider
