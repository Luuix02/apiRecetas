from flask import Flask , request, jsonify
from flask_pymongo import PyMongo , ObjectId
from flask_cors  import CORS

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://luisavilla:luuix02@cluster0.ee3ls57.mongodb.net/recetas?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)
CORS(app)
db = mongo.db.recipes

#Para crear recetas
@app.route('/recipes', methods=['POST'])
def createRecipe():
    recipe_data = {
        'nombre_receta': request.json['nombre_receta'],
        'ingredientes': request.json['ingredientes'],
        'instrucciones': request.json['instrucciones'],
        'categoria': request.json['categoria'],
        'tiempo_preparacion': request.json['tiempo_preparacion'],
        'imagen': request.json['imagen']
    }
    result = db.recipes.insert_one(recipe_data)
    print("Receta insertada con ID:", result.inserted_id)
    return jsonify({'id': str(result.inserted_id)})
    


#Para enlistar recetas
@app.route('/recipes', methods=['GET'])
def getRecipes():
      recipes = db.recipes.find({})
      formatted_recipes = []
      for recipe in recipes:
        formatted_recipe = {
            '_id': str(recipe.get('_id')),
            'nombre_receta': recipe.get('nombre_receta'),
            'ingredientes': recipe.get('ingredientes', []),
            'instrucciones': recipe.get('instrucciones'),
            'categoria': recipe.get('categoria'),
            'tiempo_preparacion': recipe.get('tiempo_preparacion'),
            'imagen': recipe.get('imagen')
        }
        formatted_recipes.append(formatted_recipe)
      return jsonify(formatted_recipes)


#Para enlistar recetas por id
@app.route('/recipes/<id>', methods=['GET'])
def getRecipe(id):
    recipe = db.recipes.find_one({'_id': ObjectId(id)})
    if recipe is None:
        return jsonify({'message': 'Receta no encontrada'}), 404
    return jsonify({
        '_id': str(ObjectId(recipe['_id'])),
        'nombre_receta': recipe.get('nombre_receta'),
        'ingredientes': recipe.get('ingredientes', []),
        'instrucciones': recipe.get('instrucciones'),
        'categoria': recipe.get('categoria'),
        'tiempo_preparacion': recipe.get('tiempo_preparacion'),
        'imagen': recipe.get('imagen')
    })


#Para eliminar recetas
@app.route('/recipes/<id>', methods=['DELETE'])
def deleteRecipe(id):
    db.recipes.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg' : 'Receta eliminada'})

    


#Para actualizar recetas por id
@app.route('/recipes/<id>', methods=['PUT'])
def updateRecipe(id):
    db.recipes.update_one({'_id' : ObjectId(id)}, {'$set': {
        'nombre_receta' : request.json['nombre_receta'],
        'ingredientes': request.json.get('ingredientes', [] ),
        'instrucciones': request.json.get('instrucciones'),
        'categoria': request.json.get('categoria'),
        'tiempo_preparacion': request.json.get('tiempo_preparacion'),
        'imagen': request.json.get('imagen')

    }})
    return jsonify({'msg' : 'Receta actualizada'})
   

if __name__ == "__main__":
    app.run(debug=True)
