import betfairlightweight
from betfairlightweight import filters

username = 'travisavery82@gmail.com'
password = 'C@mpb3ll2010'
app_key='7sd08M7xLkS2Zujv'
# app_key='K3qb3dml1HC82XZg'


# create trading instance
trading = betfairlightweight.APIClient(username=username, password=password, app_key=app_key)

print('logging in')
# login
trading.login()
print('logged in')

# make event type request to find horse racing event type
horse_racing_event_type_id = trading.betting.list_event_types(
    filter=filters.market_filter(
        # market_ids=['1.162169484']
        #text_query='Greyhound Racing'
        #text_query='Horse Racing',
        # text_query='Tennis'
        # in_play_only=
    )
)

# returns one result
# print(horse_racing_event_type_id)

for event_type in horse_racing_event_type_id:
    # prints id, name and market count

    horse_racing_id = event_type.event_type.id
    
    # print(horse_racing_id)

    # list all horse racing market catalogues
    market_catalogues = trading.betting.list_market_catalogue(
        filter=filters.market_filter(
            event_type_ids=[horse_racing_id],  # filter on just horse racing
            market_countries=['GB'],  # filter on just GB countries
            market_type_codes=['WIN'],  # filter on just WIN market types
        ),
        market_projection=['MARKET_START_TIME', 'RUNNER_DESCRIPTION'],  # runner description required
        max_results=1
    )

    if market_catalogues:
        print(event_type)

    #print('%s market catalogues returned' % len(market_catalogues))

    for market_catalogue in market_catalogues:
        # prints market id, market name and market start time
        # print('Market:',
            # market_catalogue.market_id,
            # market_catalogue.market_name,
            # market_catalogue.market_start_time
        # )

        runner_lookup = {}

        for runner in market_catalogue.runners:
            # prints runner id, runner name and handicap
            # print('Runner:', runner.selection_id, runner.runner_name, runner.handicap)
            runner_lookup[runner.selection_id] = runner.runner_name

        # # market book request

        market_books = trading.betting.list_market_book(
            market_ids=[market_catalogue.market_id],
            price_projection=filters.price_projection(
                price_data=filters.price_data(
                    ex_all_offers=True
                )
            )
        )


        for market_book in market_books:
            # prints market id, inplay?, status and total matched
            print('Market: {}, InPlay: {}, Status: {}, Total Matched: {}'.format(
                    market_book.market_id,
                    market_book.inplay,
                    market_book.status,
                    market_book.total_matched
                )
            )
            
            print('Book:')

            for runner in market_book.runners:
                # prints selection id, status and total matched
                print("'{}' {}".format(
                        ' '.join(runner_lookup[runner.selection_id].split()[1:]),
                        # runner.status,
                        runner.total_matched if runner.total_matched else ''
                    )
                )

                available_to_back = sorted(runner.ex.available_to_back, key=lambda t: t.price, reverse=True)
                available_to_lay = runner.ex.available_to_lay
                print('Back:', available_to_back)
                print('Lay: ', available_to_lay)



# logout
trading.logout()