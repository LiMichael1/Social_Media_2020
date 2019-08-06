import twitter
import pandas as pd
import matplotlib.pyplot as plt
import statistics

presidential_candidates = ('Joe Biden', 'Bernie Sanders', 'Elizabeth Warren', 'Kamala Harris', 'Pete Buttigieg',
                           'Cory Booker', 'Julian Castro', 'Amy Klobuchar', 'Beto O\' Rourke', 'Kirsten Gillibrand',
                           'Tulsi Gabbard', 'Andrew Yang', 'Bill de Blasio')

class presidential_candidate(object):
    def __init__(self, name, pos, neg):
        self._name = name
        self._pos = pos
        self._neg = neg
        self._neu = round(100 - pos - neg,2)

def BarGraph (df):
    f, ax = plt.subplots(1, figsize=(10,5))

    bar_width = 1
    #bar positions
    bar_l = [i for i in range(len(df['Positive']))]

    #center  position for the bars
    tick_pos = [i + (bar_width/2) for i in bar_l]

    pos = [i for i in df['Positive']]
    neg = [i for i in df['Negative']]
    neu = [i for i in df['Neutral']]



    #POSITIVE BAR
    ax.bar(bar_l,
           pos,
           label='Positive',
           alpha=0.9,
           color='#00FF00',
           width=bar_width,
           edgecolor='white'
           )

    #NEGATIVE BAR
    ax.bar(bar_l,
           neg,
           bottom=pos,
           label='Negative',
           alpha=0.9,
           color='#FF0000',
           width=bar_width,
           edgecolor='white'
           )

    #NEUTRAL BAR
    ax.bar(bar_l,
           neu,
           bottom=[i + j for i, j in zip(pos, neg)],
           label='Neutral',
           alpha=0.9,
           color='#C0C0C0',
           width=bar_width,
           edgecolor='white'
           )

    # Set the ticks to be first names
    plt.xticks(tick_pos, df['Name'])
    ax.set_ylabel("Percentage")
    ax.set_xlabel("")

    # Let the borders of the graphic
    plt.xlim([min(tick_pos) - bar_width, max(tick_pos) + bar_width])
    plt.ylim(-10, 110)

    # rotate axis labels
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

    # shot plot
    plt.savefig('bar_graph.png', bbox_inches='tight')




def main():
    api = twitter.TwitterClient()
    candidate_list = []
    for candidate_name in presidential_candidates:
        pos_list = []
        neg_list = []
        for i in range(8):
            #print (candidate_name)
            tweets = api.get_tweets(query = candidate_name, count = 1000)
            positive, negative = twitter.PosNegTweets(tweets)
            pos_list.append(positive)
            neg_list.append(negative)
        pos_avg = round(statistics.mean(pos_list),2)
        neg_avg = round(statistics.mean(neg_list),2)
        Dem = presidential_candidate(candidate_name, pos_avg, neg_avg)
        candidate_list.append(Dem)

    pos = (i._pos for i in candidate_list)
    neg = (j._neg for j in candidate_list)
    neu = (k._neu for k in candidate_list)

    data = [[i,j,k,l] for i, j, k, l in zip(presidential_candidates, pos, neg, neu)]

    df = pd.DataFrame(data, columns = ['Name','Positive', 'Negative', 'Neutral'])
    print(df['Name'])
    BarGraph(df)

if __name__ == "__main__":
    main()